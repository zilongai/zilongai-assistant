# 子龙AI 助手 / ZilongAI Assistant

把电脑上的 Claude Code、Codex 一键接到子龙AI。不用注册、不用邮箱，输入卡密就能用。

Connects Claude Code and Codex on your PC to ZilongAI in one click. No sign-up and no email: enter a card code and start.

## 下载安装

**0.3.46：Claude Code 和 Codex 的模型列表自动跟随服务器更新。首次升级后，请等当前任务结束，再重新接管并重启所用工具；之后新增模型无需再次更新助手。Claude Code 每分钟检查，Codex 约每 4 分半刷新。Claude 桌面版在下次正常启动时重新获取列表。关闭接管或正常退出仍恢复原配置。**

**[下载 Windows 安装包](https://github.com/zilongai/zilongai-assistant/releases/latest/download/zilongai-assistant_x64-setup.exe)**：点一下就开始下载，总是最新版，以后会自动更新。朋友也要用的话，转发这个链接就行，不用发压缩包。

**Mac Apple 芯片版 0.3.46：[首次安装／旧版升级（DMG）](https://github.com/zilongai/zilongai-assistant/releases/download/mac-v0.3.46/zilongai-assistant_0.3.46_aarch64.dmg)**。0.3.40 起可在助手里点「检查更新 → 重启更新」下载、安装并自动重启。0.3.39 及更早的 Mac 版需先安装一次本版：退出旧版助手，打开 DMG，将「子龙AI 助手」拖入「应用程序」并替换旧版，再重新打开。不支持 Intel Mac。首次打开被 macOS 提示拦下时，在「系统设置 → 隐私与安全性」中选择「仍要打开」。系统要求读取钥匙串时请允许；取消后可在助手中重试，无需重新开通账户。应用采用临时签名，尚未经过 Apple 公证。

**Linux x64 版 0.3.46（Ubuntu 桌面）：[deb 安装包](https://github.com/zilongai/zilongai-assistant/releases/download/linux-v0.3.46/zilongai-assistant_0.3.46_amd64.deb) · [AppImage](https://github.com/zilongai/zilongai-assistant/releases/download/linux-v0.3.46/zilongai-assistant_0.3.46_amd64.AppImage)**。deb 可用系统软件安装器安装；AppImage 在文件属性中允许作为程序执行后打开。支持 Claude Code、Codex 命令行版、知识库和签名更新。首次使用请让系统密码库解锁；deb 更新需要系统安装授权。

**打不开 GitHub**（例如在中国大陆）时，请联系向您提供卡密的代理或客服获取下载方式。

1. 准备一台 Windows 10 / 11（64 位）电脑，Apple 芯片 Mac 使用上方的 Mac 安装包；不支持 Intel Mac。Claude Code、Codex 没装也可以，开通后在助手里一键安装。Codex 命令行版在官方下载不了时，会自动改从国内镜像下载同一份官方程序并核对校验值；Windows 上的 Codex 客户端只能从微软商店装，商店装不上可以改用命令行版。
2. 下载安装包。浏览器如提示「不常下载」，选择「保留」。
3. 运行安装包。如出现「Windows 已保护你的电脑」，点击「更多信息」，再点击「仍要运行」。安装包尚未购买代码签名证书；请只从可信的下载链接获取。软件安装在当前用户目录，不需要管理员权限。
4. 打开「子龙AI 助手」，粘贴卡密，点击「开通」，并记下账户号：换电脑时要用它和卡密一起找回账户。开通需要「子龙AI 助手专用」卡密，其他卡密不能用来开通。
5. 在首页打开 Claude Code、Codex 的开关，就可以使用了。

界面语言跟随系统，也可以在「设置」里切换中文或英文。遇到问题，点击助手里的「联系客服」，还没开通也能留言。0.3.44 起，开通后的留言可以带图片和文件：截图直接粘贴，文件拖进窗口，或点回形针（图片 10 MB、文件 20 MB 以内）。

Linux 校验值见 [Linux 发布页](https://github.com/zilongai/zilongai-assistant/releases/tag/linux-v0.3.46)的 `SHA256SUMS-Linux.txt`。

Windows 安装包的 SHA-256 指纹在 `SHA256SUMS.txt` 中，Mac 包在[对应 Mac 发布页](https://github.com/zilongai/zilongai-assistant/releases/tag/mac-v0.3.46)的 `SHA256SUMS-macOS.txt` 中。Windows 下载后可在 PowerShell 中运行以下命令，并与文件中的指纹核对：

```powershell
Get-FileHash .\zilongai-assistant_x64-setup.exe -Algorithm SHA256
```

Mac 可在终端运行 `shasum -a 256 ~/Downloads/zilongai-assistant_0.3.46_aarch64.dmg` 核对。

## Download and install

**0.3.46 keeps Claude Code and Codex model lists synchronized with the server. After this first upgrade, finish your current task, apply takeover again, and restart the tool. Later model additions do not require another assistant update. Claude Code checks every minute; Codex refreshes about every 4.5 minutes. The Claude desktop app fetches the directory on its next normal startup. Disabling takeover or quitting still restores the previous configuration.**

**[Download the Windows installer](https://github.com/zilongai/zilongai-assistant/releases/latest/download/zilongai-assistant_x64-setup.exe)**: one click starts the download. It is always the latest version and updates itself after that. If a friend wants it too, just send this link; there is no zip file to pass around.

**Apple silicon Mac 0.3.46: [First installation / upgrade from older versions (DMG)](https://github.com/zilongai/zilongai-assistant/releases/download/mac-v0.3.46/zilongai-assistant_0.3.46_aarch64.dmg)**. From 0.3.40, choose **Check for updates → Restart to update** in the assistant to download, install and restart automatically. Mac versions 0.3.39 and earlier require this one initial installation: quit the assistant, open the DMG, replace the app in Applications, then reopen it. Intel Macs are not supported. If macOS prompts on first launch, use System Settings → Privacy & Security → Open Anyway. Allow Keychain access when requested; if cancelled, retry in the assistant without activating a new account. The app is ad-hoc signed and is not Apple-notarized.

**Linux x64 0.3.46 (Ubuntu desktop): [Debian package](https://github.com/zilongai/zilongai-assistant/releases/download/linux-v0.3.46/zilongai-assistant_0.3.46_amd64.deb) · [AppImage](https://github.com/zilongai/zilongai-assistant/releases/download/linux-v0.3.46/zilongai-assistant_0.3.46_amd64.AppImage)**. Install the deb with your system software installer, or allow the AppImage to run as a program in its file properties. Includes Claude Code and Codex CLI integration, the knowledge base and signed updates. Unlock the system keyring when requested; deb updates need system installation approval.

**If GitHub does not open** (for example in mainland China), contact your reseller or support for a way to download it.

1. Use a 64-bit Windows 10 or 11 PC, or download the Mac package above for an Apple silicon Mac. Intel Macs are not supported. You do not need Claude Code or Codex installed already: after activation, the assistant can install them in one click. If the official Codex CLI download is unavailable, the assistant downloads the same official program from a mirror in China and verifies its checksum. On Windows, the Codex app comes only from the Microsoft Store; if the Store cannot install it, you can use the command-line version instead.
2. Download the installer. If the browser says it is not commonly downloaded, choose **Keep**.
3. Run the installer. If Windows displays **Windows protected your PC**, choose **More info**, then **Run anyway**. The installer does not yet have a purchased code-signing certificate; use only a trusted download link. It installs in your user directory and does not require administrator privileges.
4. Open ZilongAI Assistant, paste your card code and choose **Activate**. Write down your account number: you need it with a card code to restore your account on a new computer. Activation requires a ZilongAI Assistant card code; other card codes cannot be used.
5. Turn on the Claude Code and Codex switches on the Overview page, and you are ready.

The interface follows your system language, and you can switch between Chinese and English in **Settings**. If you run into trouble, choose **Contact support** in the assistant. It works even before activation. The full guide and troubleshooting are in the [User Guide](USER_GUIDE.md).

Linux checksums are in `SHA256SUMS-Linux.txt` on the [Linux release page](https://github.com/zilongai/zilongai-assistant/releases/tag/linux-v0.3.46).

Windows checksums are in `SHA256SUMS.txt`; Mac checksums are in `SHA256SUMS-macOS.txt` on the [Mac release page](https://github.com/zilongai/zilongai-assistant/releases/tag/mac-v0.3.46). Use the PowerShell command above for Windows, or `shasum -a 256 ~/Downloads/zilongai-assistant_0.3.46_aarch64.dmg` on Mac, and compare with the relevant file.

## 联系 / Contact

请联系向您提供卡密的代理或客服。 / Please contact your reseller or support.

## 声明 / Notice

本软件为闭源软件，本仓库只提供安装包及发布相关文件。保留所有权利。子龙AI 与 Anthropic、OpenAI 均无关联。

This software is closed source. This repository provides installers and release-related files only. All rights reserved. ZilongAI is not affiliated with Anthropic or OpenAI.
