"""Offline tests: HTTP, the verifier and all gh invocations are fakes."""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'sync_release.py'
SPEC = importlib.util.spec_from_file_location('sync_release', SCRIPT)
sync = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync)


class Response(io.BytesIO):
    def __init__(self, data=b'', status=200, headers=None):
        super().__init__(data)
        self.status = status
        self.headers = headers or {}


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name) / 'work'
        base = mock.patch.object(sync, 'BASE', 'https://updates.example.invalid')
        base.start()
        self.addCleanup(base.stop)
        self.content = b'test-only installer bytes'
        self.digest = hashlib.sha256(self.content).hexdigest()
        self.manifest = {
            'version': '1.2.3',
            'url': f'{sync.BASE}/api/v1/desktop/update/files/zilongai-assistant_1.2.3_x64-setup.exe',
            'signature': 'fake signed data',
            'pub_date': '2026-11-01T00:00:00Z',
            'notes': 'Updates / 更新',
        }
        self.calls = []
        self.created = None
        self.view = subprocess.CompletedProcess([], 1, '', 'release not found\n')
        self.create_rc = 0
        self.verified = True

    def fake_open(self, url):
        self.calls.append(('http', url))
        if '/update/windows/' in url:
            return Response(json.dumps(self.manifest).encode('utf-8'))
        if url == self.manifest['url']:
            return Response(self.content, headers={'Content-Length': str(len(self.content))})
        raise AssertionError('unexpected URL')

    def fake_gh(self, command, **kwargs):
        self.calls.append(('gh', command))
        self.assertEqual(kwargs, {'capture_output': True, 'text': True, 'timeout': sync.GH_TIMEOUT_SECONDS, 'check': False})
        if command[1:3] == ['release', 'view']:
            return self.view
        self.assertEqual(command[1:3], ['release', 'create'])
        notes_path = Path(command[command.index('--notes-file') + 1])
        self.created = {
            'args': command,
            'notes': notes_path.read_text(encoding='utf-8'),
            'installer_name': Path(command[-2]).name,
            'installer': Path(command[-2]).read_bytes(),
            'sums': Path(command[-1]).read_text(encoding='utf-8'),
        }
        return subprocess.CompletedProcess(command, self.create_rc, '', '')

    def fake_verify(self, file, sig):
        self.assertEqual(file.read_bytes(), self.content)
        self.assertEqual(sig.read_text(encoding='utf-8'), self.manifest['signature'])
        return {'file_signature_valid': self.verified, 'trusted_comment_valid': self.verified, 'file_sha256': self.digest}

    def run_sync(self, extra=None):
        out, err = io.StringIO(), io.StringIO()
        args = ['--work-dir', str(self.work)] + (extra or [])
        with mock.patch.object(sync, 'open_url', side_effect=self.fake_open), \
             mock.patch.object(sync.subprocess, 'run', side_effect=self.fake_gh), \
             mock.patch.object(sync.verify_tauri_sig, 'verify', side_effect=self.fake_verify), \
             redirect_stdout(out), redirect_stderr(err):
            code = sync.main(args)
        return code, out.getvalue(), err.getvalue()

    def test_missing_base_fails_before_network(self):
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sync, 'BASE', ''), mock.patch.object(sync, 'open_url', self.fake_open), redirect_stdout(out), redirect_stderr(err):
            code = sync.main(['--work-dir', str(self.work)])
        self.assertEqual(code, 2)
        self.assertEqual(self.calls, [])

    def test_204_skips_without_gh(self):
        self.fake_open = lambda url: Response(status=204)
        code, out, _ = self.run_sync()
        self.assertEqual(code, 0)
        self.assertIn('stable 为空，跳过', out)
        self.assertFalse(self.calls)
        self.assertFalse(self.work.exists())

    def test_bad_version_rejected_before_gh(self):
        for version in ('v1.2.3', '1.2', '../1.2.3', '１.２.３'):
            with self.subTest(version=version):
                self.manifest['version'] = version
                code, _, err = self.run_sync()
                self.assertEqual(code, 2)
                self.assertIn('版本号', err)
                self.assertFalse(any(kind == 'gh' for kind, _ in self.calls))

    def test_wrong_url_rejected_before_gh(self):
        self.manifest['url'] += '?extra=1'
        code, _, err = self.run_sync()
        self.assertEqual(code, 2)
        self.assertIn('地址', err)
        self.assertFalse(any(kind == 'gh' for kind, _ in self.calls))

    def test_empty_signature_rejected(self):
        self.manifest['signature'] = ' '
        code, _, err = self.run_sync()
        self.assertEqual(code, 2)
        self.assertIn('签名', err)
        self.assertFalse(any(kind == 'gh' for kind, _ in self.calls))

    def test_invalid_unicode_in_notes_rejected_before_gh(self):
        self.manifest['notes'] = '\ud800'
        code, _, err = self.run_sync()
        self.assertEqual(code, 2)
        self.assertIn('编码', err)
        self.assertFalse(any(kind == 'gh' for kind, _ in self.calls))

    def test_existing_release_skips_download(self):
        self.view = subprocess.CompletedProcess([], 0, 'existing', '')
        code, out, _ = self.run_sync()
        self.assertEqual(code, 0)
        self.assertIn('已发布，跳过', out)
        self.assertEqual(sum(kind == 'http' for kind, _ in self.calls), 1)
        self.assertIsNone(self.created)

    def test_failed_verification_never_creates_release(self):
        self.verified = False
        code, _, err = self.run_sync()
        self.assertEqual(code, 3)
        self.assertIn('验签失败', err)
        self.assertIsNone(self.created)
        self.assertEqual(list(self.work.iterdir()), [])

    def test_successful_release_checksums_and_notes(self):
        code, out, _ = self.run_sync()
        self.assertEqual(code, 0)
        self.assertIn(self.digest, out)
        self.assertEqual(self.created['installer_name'], sync.FIXED_NAME)
        self.assertEqual(self.created['installer'], self.content)
        self.assertEqual(self.created['sums'],
                         f'{self.digest}  {sync.FIXED_NAME}\n'
                         f'{self.digest}  zilongai-assistant_1.2.3_x64-setup.exe\n')
        self.assertIn('## 中文', self.created['notes'])
        self.assertIn('## English', self.created['notes'])
        self.assertIn(self.manifest['pub_date'], self.created['notes'])
        self.assertIn(self.manifest['notes'], self.created['notes'])
        self.assertNotIn(sync.BASE, self.created['notes'])
        self.assertNotIn('备用', self.created['notes'])
        self.assertNotIn('Mainland China', self.created['notes'])
        self.assertIn('--latest', self.created['args'])
        self.assertEqual(list(self.work.iterdir()), [])

    def test_nonstable_without_dry_run_rejected_before_network(self):
        code, _, err = self.run_sync(['--channel', 'beta'])
        self.assertEqual(code, 2)
        self.assertIn('只能用于 --dry-run', err)
        self.assertFalse(self.calls)

    def test_beta_dry_run_does_not_create(self):
        code, out, _ = self.run_sync(['--channel', 'beta', '--dry-run'])
        self.assertEqual(code, 0)
        self.assertIn('gh release create v1.2.3', out)
        self.assertIsNone(self.created)
        self.assertIn('channel=beta', self.calls[0][1])
        self.assertEqual(list(self.work.iterdir()), [])

    def test_missing_repo_only_tolerated_in_dry_run(self):
        self.view = subprocess.CompletedProcess([], 1, '', 'GraphQL: Could not resolve to a Repository with the name test/missing. (repository)')
        code, out, _ = self.run_sync(['--dry-run'])
        self.assertEqual(code, 0)
        self.assertIn('按未发布处理', out)
        self.assertIsNone(self.created)
        self.calls.clear()
        code, _, _ = self.run_sync()
        self.assertEqual(code, 5)
        self.assertIsNone(self.created)

    def test_gh_error_is_not_treated_as_missing_or_echoed(self):
        self.view = subprocess.CompletedProcess([], 1, '', 'authentication failed: sensitive-value')
        code, out, err = self.run_sync()
        self.assertEqual(code, 5)
        self.assertNotIn('sensitive-value', out + err)
        self.assertIsNone(self.created)
        self.assertEqual(sum(kind == 'http' for kind, _ in self.calls), 1)

    def test_gh_create_failure_returns_five(self):
        self.create_rc = 1
        code, _, err = self.run_sync()
        self.assertEqual(code, 5)
        self.assertIn('发布失败', err)
        self.assertEqual(list(self.work.iterdir()), [])

    def test_download_size_limit_without_content_length(self):
        def open_unbounded(url):
            if '/update/windows/' in url:
                return Response(json.dumps(self.manifest).encode('utf-8'))
            return Response(self.content)
        self.fake_open = open_unbounded
        with mock.patch.object(sync, 'MAX_INSTALLER_BYTES', 4):
            code, _, err = self.run_sync()
        self.assertEqual(code, 4)
        self.assertIn('大小超过限制', err)
        self.assertIsNone(self.created)

    def test_download_truncation_is_rejected(self):
        def open_short(url):
            if '/update/windows/' in url:
                return Response(json.dumps(self.manifest).encode('utf-8'))
            return Response(self.content, headers={'Content-Length': str(len(self.content) + 1)})
        self.fake_open = open_short
        code, _, err = self.run_sync()
        self.assertEqual(code, 4)
        self.assertIn('长度不符', err)
        self.assertIsNone(self.created)

    def test_malformed_manifest_fails(self):
        self.fake_open = lambda url: Response(b'not json')
        code, _, err = self.run_sync()
        self.assertEqual(code, 2)
        self.assertIn('JSON', err)
        self.assertFalse(any(kind == 'gh' for kind, _ in self.calls))


if __name__ == '__main__':
    unittest.main()
