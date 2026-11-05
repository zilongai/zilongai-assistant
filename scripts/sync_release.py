"""Synchronize a signed stable Windows updater release to GitHub."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from urllib import error, parse, request

BASE = os.environ.get('RELEASE_BASE_URL', '').rstrip('/')
FIXED_NAME = 'zilongai-assistant_x64-setup.exe'
MAX_INSTALLER_BYTES = 200 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
NETWORK_TIMEOUT_SECONDS = 30
GH_TIMEOUT_SECONDS = 60

# -I removes the script directory from sys.path. Load the adjacent, pinned
# verifier explicitly rather than depending on the runner's Python environment.
_spec = importlib.util.spec_from_file_location('verify_tauri_sig', Path(__file__).with_name('verify_tauri_sig.py'))
verify_tauri_sig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(verify_tauri_sig)


class Failure(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message


class ChineseParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, '参数错误：请检查必填参数和选项。\n')


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise error.URLError('redirect rejected')


def open_url(url):
    req = request.Request(url, headers={'Accept': 'application/json, application/octet-stream', 'User-Agent': 'ZilongAI-Release-Sync'})
    return request.build_opener(NoRedirect()).open(req, timeout=NETWORK_TIMEOUT_SECONDS)


def read_manifest(channel):
    query = parse.urlencode({'channel': channel})
    url = f'{BASE}/api/v1/desktop/update/windows/x86_64/0.0.1?{query}'
    try:
        with open_url(url) as response:
            if response.status == 204:
                return None
            if response.status != 200:
                raise Failure(4, '清单请求失败：服务返回了非预期状态。')
            data = response.read(MAX_MANIFEST_BYTES + 1)
    except Failure:
        raise
    except (OSError, error.URLError, TimeoutError):
        raise Failure(4, '清单请求失败：网络不可用或请求超时。') from None
    if len(data) > MAX_MANIFEST_BYTES:
        raise Failure(2, '清单格式错误：内容超过大小限制。')
    try:
        manifest = json.loads(data.decode('utf-8'))
    except (ValueError, UnicodeError):
        raise Failure(2, '清单格式错误：无法解析 JSON。') from None
    return validate_manifest(manifest)


def validate_manifest(manifest):
    if not isinstance(manifest, dict):
        raise Failure(2, '清单格式错误：顶层不是对象。')
    version = manifest.get('version')
    if not isinstance(version, str) or len(version) > 64 or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version):
        raise Failure(2, '清单格式错误：版本号不符合要求。')
    versioned_name = f'zilongai-assistant_{version}_x64-setup.exe'
    expected_url = f'{BASE}/api/v1/desktop/update/files/{versioned_name}'
    if manifest.get('url') != expected_url:
        raise Failure(2, '清单格式错误：安装包地址与版本不匹配。')
    signature = manifest.get('signature')
    if not isinstance(signature, str) or not signature.strip() or len(signature) > 16384:
        raise Failure(2, '清单格式错误：签名为空或过长。')
    for key in ('pub_date', 'notes'):
        value = manifest.get(key)
        if value is not None and not isinstance(value, str):
            raise Failure(2, '清单格式错误：日期或说明不是文本。')
    try:
        for value in (signature, manifest.get('pub_date') or '', manifest.get('notes') or ''):
            value.encode('utf-8')
    except UnicodeError:
        raise Failure(2, '清单格式错误：文本编码无效。') from None
    return manifest, versioned_name


def run_gh(args):
    try:
        return subprocess.run(['gh', *args], capture_output=True, text=True, timeout=GH_TIMEOUT_SECONDS, check=False)
    except (OSError, subprocess.TimeoutExpired):
        raise Failure(5, 'GitHub 检查失败：gh 不可用或请求超时。') from None


def release_exists(version, dry_run):
    result = run_gh(['release', 'view', f'v{version}'])
    if result.returncode == 0:
        return True
    # Do not mistake authentication, network or permission errors for absence.
    message = result.stderr.strip().lower()
    if message == 'release not found':
        return False
    if dry_run and 'could not resolve to a repository with the name' in message:
        print('仓库尚不存在或不可访问，演练按未发布处理。')
        return False
    raise Failure(5, 'GitHub 检查失败：无法确认该版本是否已发布。')


def download_installer(url, destination):
    try:
        with open_url(url) as response, destination.open('xb') as target:
            if response.status != 200:
                raise Failure(4, '安装包下载失败：服务返回了非预期状态。')
            length = response.headers.get('Content-Length')
            if length is not None:
                if not length.isascii() or not length.isdigit() or int(length) > MAX_INSTALLER_BYTES:
                    raise Failure(4, '安装包下载失败：大小超过限制或响应无效。')
            total = 0
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_INSTALLER_BYTES:
                    raise Failure(4, '安装包下载失败：大小超过限制。')
                target.write(chunk)
            if total == 0 or (length is not None and total != int(length)):
                raise Failure(4, '安装包下载失败：文件为空或长度不符。')
    except Failure:
        raise
    except (OSError, error.URLError, TimeoutError):
        raise Failure(4, '安装包下载失败：网络、文件或超时错误。') from None


def release_notes(manifest, sha256):
    version = manifest['version']
    date = manifest.get('pub_date') or ''
    notes = manifest.get('notes') or ''
    return (
        f'## 中文\n\n版本：{version}\n\n发布日期：{date}\n\n更新说明：\n\n{notes}\n\n'
        f'SHA-256：`{sha256}`\n\n'
        f'## English\n\nVersion: {version}\n\nPublication date: {date}\n\nRelease notes:\n\n{notes}\n\n'
        f'SHA-256: `{sha256}`\n'
    )


def sync(args):
    if not re.fullmatch(r'[a-z0-9_-]{1,32}', args.channel):
        raise Failure(2, '参数错误：通道名称无效。')
    if not BASE:
        raise Failure(2, '配置错误：没有设置发布地址。')
    if args.channel != 'stable' and not args.dry_run:
        raise Failure(2, '参数错误：非 stable 通道只能用于 --dry-run 演练。')
    result = read_manifest(args.channel)
    if result is None:
        print(f'{args.channel} 为空，跳过')
        return
    manifest, versioned_name = result
    version = manifest['version']
    if release_exists(version, args.dry_run):
        print('已发布，跳过')
        return
    try:
        args.work_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='sync-release-', dir=args.work_dir) as temporary:
            work = Path(temporary)
            original = work / versioned_name
            signature = work / (versioned_name + '.sig')
            download_installer(manifest['url'], original)
            signature.write_text(manifest['signature'], encoding='utf-8')
            try:
                checked = verify_tauri_sig.verify(original, signature)
            except (OSError, ValueError, UnicodeError, IndexError):
                raise Failure(3, '验签失败：签名或文件无效。') from None
            if not checked['file_signature_valid'] or not checked['trusted_comment_valid']:
                raise Failure(3, '验签失败：安装包或签名不匹配。')
            sha256 = checked['file_sha256']
            fixed = work / FIXED_NAME
            shutil.copyfile(original, fixed)
            sums = work / 'SHA256SUMS.txt'
            sums.write_text(f'{sha256}  {FIXED_NAME}\n{sha256}  {versioned_name}\n', encoding='utf-8')
            notes = work / 'release-notes.md'
            notes.write_text(release_notes(manifest, sha256), encoding='utf-8')
            command = ['release', 'create', f'v{version}', '--title', f'v{version}', '--notes-file', str(notes), '--latest', str(fixed), str(sums)]
            print(f'SHA-256: {sha256}')
            if args.dry_run:
                print('演练命令：' + shlex.join(['gh', *command]))
            elif run_gh(command).returncode != 0:
                raise Failure(5, 'GitHub 发布失败：gh 未能创建 Release。')
            else:
                print('Release 已发布。')
    except Failure:
        raise
    except OSError:
        raise Failure(4, '准备发布文件失败：临时目录不可用。') from None


def main(argv=None):
    parser = ChineseParser(description=__doc__)
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--channel', default='stable')
    args = parser.parse_args(argv)
    try:
        sync(args)
    except Failure as exc:
        print(exc.message, file=sys.stderr)
        return exc.code
    return 0


if __name__ == '__main__':
    sys.exit(main())
