# ZilongAI Assistant: User Guide

Updated for version 0.3.39. Windows updates are delivered through the assistant.

## Before you start

- A 64-bit Windows 10 or 11 PC, or an Apple silicon Mac. [Download the Mac 0.3.39 DMG](https://github.com/zilongai/zilongai-assistant/releases/download/v0.3.39/zilongai-assistant_aarch64.dmg). Mac updates require manual installation: quit the assistant, open the DMG, drag it into Applications and replace the previous version, then reopen it. Intel Macs are not supported.
- Claude Code and Codex are optional. If you already have them (command line, VS Code extension or desktop app), the assistant takes them over directly. If not, install them from the assistant after activation.
- A ZilongAI Assistant card code. Other card codes cannot be used for activation.

## Step 1: Download and install

1. Download the Windows installer: https://github.com/zilongai/zilongai-assistant/releases/latest/download/zilongai-assistant_x64-setup.exe

   It is always the latest version. If a friend wants it too, just send this link; there is no zip file to pass around. If GitHub does not open (for example in mainland China), contact the seller of your card.

   To verify the installer, compare it with the SHA-256 in https://github.com/zilongai/zilongai-assistant/releases/latest/download/SHA256SUMS.txt
2. If your browser says the file is not commonly downloaded, choose **Keep**.
3. Run the installer. If a blue window says **Windows protected your PC**, choose **More info**, then **Run anyway**.

   You see this because the installer does not yet have a purchased code-signing certificate. It is not a virus warning. Download only from the link above.
4. It installs in your own user folder and does not need administrator rights.

## Step 2: Activate with your card code

1. Open ZilongAI Assistant. On first launch it checks for a newer version, updates itself and reopens. If your network prevents the update, you can activate with the current version.
2. Paste your 32-character code into **Card code** (dashes are fine) and choose **Activate**.
3. You then see your **account number**, which looks like `ZL-7KQ4-M2XB`.
4. **Take a screenshot or write it down right away.** To restore your account after changing computers or reinstalling Windows, you need both a card code you used and this account number. You can also find it at the bottom of the sidebar and in **Settings**.
5. The account number is not a password. Nobody can sign in with it alone.
6. **Contact support** is at the bottom of the activation page and works before activation. You get a notification when support replies. Support knows you by the computer number shown there.
7. The assistant does not change your Claude Code or Codex settings before activation. If this PC was signed in before (for example, you reinstalled the assistant), you see **This computer was signed in to ZilongAI before**. If that account is yours, choose **Keep using this account**. If it is not yours or you are unsure, choose **Not mine, enter a new card**.

## Step 3: Connect Claude Code and Codex

1. Turn on the Claude Code and Codex switches on the **Overview** page. The assistant connects them to ZilongAI.
2. You do not need a terminal. **Open app** opens the desktop app: the Codex app is now part of the ChatGPT app, and the Claude app is Claude's desktop app. **Open terminal** appears only when the command-line version is installed, and starts it in a new terminal window in your last project folder. Once connected, the Claude app uses ZilongAI with no Claude sign-in. When you quit the assistant, its original sign-in comes back.
3. If something is not installed, install it from the assistant:
   - Choose **Install app** for a desktop app or **Install CLI** for a command-line version. After you confirm, the button shows download and install progress. When it finishes, you are told what to click next, and it connects to ZilongAI automatically.
   - This is the official software, downloaded from the official source and checked. It goes in your user folder with no administrator rights. It updates itself, and quitting or uninstalling the assistant does not remove it.
   - The Codex app (listed as ChatGPT in the Microsoft Store) comes only from the Microsoft Store. The assistant installs it for you. If it cannot, the Store page opens: choose **Get**, then come back and choose **Open app**. If the Store does not work either (for example in mainland China), choose **Install CLI** to use the command-line version instead.
   - If the official Codex CLI download is unavailable (for example in mainland China), the assistant automatically downloads the same official program from a mirror in China and verifies its checksum. You do not need to do anything.
4. Programs that were open before takeover must restart to use ZilongAI, which stops anything they are running:
   - Codex and Claude apps restart automatically and keep your conversations. If one could not restart, the **Overview** page tells you: choose **Restart app**.
   - Terminal windows: choose **Restart terminals**. They reopen in the same folders and continue the last conversation.
   - VS Code extension: reload the window.
5. If you are not sure everything is connected, choose **Run checkup**. If something is wrong, use the button next to it.
6. Closing the window keeps the assistant running in the tray. To put Claude Code and Codex back on their previous settings, choose **Quit and restore settings** in **Settings**.
7. For other tools such as Cherry Studio or Cursor, go to **Settings** > **For other tools**, choose **Copy address and token** and paste them in. The token changes when the assistant restarts, so copy it again after a restart.

## Generating images

1. With the assistant open and Claude Code or Codex connected, just ask for an image, such as "paint a watercolor fox", "make a 16:9 poster" or "change this image to blue". It uses ZilongAI image generation automatically. You do not need an OpenAI sign-in or any key.
2. Images are saved in the `outputs` folder of your current project. The reply tells you where they are and roughly how many points they used.
3. The default is 1K (1024×1024), at 6 points per image. Ask for high resolution, a wallpaper, a poster, or landscape or portrait, and it uses 2K (9 points per image) or 4K (12 points per image).
4. The first time, Claude Code may ask whether it can run `zilongai-image`. Allow it (you can choose not to be asked again). Codex uses a tool shown as `image_gen` from `zilongai`. If it asks, allow it.
5. Your own Codex rules, such as "only use the official image tool", are fine. While connected, ZilongAI image generation goes first, and your rules apply only if it fails.
6. Image generation needs the assistant running. When you quit the assistant, this feature goes away and Codex's own image settings come back. Changes you made to instructions and skills in Codex in the meantime are kept.

## Making music (0.3.31 and later)

1. With the assistant open and Claude Code or Codex connected, start a new conversation and just ask for a song, such as "make a calm piano piece with no vocals" or "write a pop song about summer". You can also give it your own lyrics. There is no sign-in and no key to enter.
2. It usually takes one to a few minutes. Songs are saved as `.m4a` files in the `outputs` folder of your current project. The reply tells you where they are and how many points they used.
3. Each song costs 100 points, and one request usually makes two songs, so 200 points. 200 points are held when it starts. If only one song is delivered, 100 come back. If it fails, all of them come back.
4. Music needs a regular card; test cards cannot make music. It works as soon as you redeem a regular card.
5. Each account can make 1 at a time and up to 5 a day. The day changes at midnight China time, and fully refunded tasks do not count.
6. Music needs the assistant running. When you quit the assistant, this feature goes away.

## Knowledge base and Obsidian (0.3.39 and later)

After takeover, the model can proactively save useful preferences, project decisions and milestone summaries, then retrieve them in a new chat. Routine memory writes do not require a confirmation prompt. Your explicit instructions, such as do not remember or ask first, take priority.

In Settings → Knowledge base, choose Automatic, Read only or Off, or select an existing knowledge folder. Changing its location does not move existing notes. Choose Open folder, then open that folder as a vault in Obsidian. No plugin is required. Notes are ordinary Markdown files and remain when the assistant exits or is uninstalled.

Changes apply to subsequent memory calls. Pausing or quitting the assistant, or disabling the corresponding takeover, stops further memory calls from existing assistant-mode MCP sessions. Content already included in a chat is not retracted. Relevant note excerpts are sent to the model as part of the conversation. Reopen the AI session if memory tools are missing after an update.

## Claude Agent SDK guide

Settings includes a Python / TypeScript setup guide. It distinguishes existing protocol compatibility from dedicated end-to-end SDK testing, which has not been completed. This release adds documentation; it does not introduce a new SDK protocol or backend change.

## Points, validity and top-ups

- The **Overview** page shows your **Points** and what you have **Used today**.
- Points are valid from activation or top-up for the card's term.
- **To top up**, choose **Top up with a card** on the **Overview** page. Your whole balance rolls over to the later of the current expiry date and today plus the new card's days.
- You get a reminder 7 days and 1 day before expiry.
- After expiry, points are frozen for 7 days and Claude Code and Codex are paused. Top up during the freeze and all your points come back. After 7 days the points are cleared. Your account number and computers stay, and the next top-up starts a new term.
- **Codex speed**: Fast and UltraFast respond faster, are billed at the official fast-lane prices and use noticeably more points. The setting on the **Overview** page decides and takes effect immediately. Typing `/fast` in Codex changes it too.

## New computer or reinstall

1. Install the assistant on the new computer and choose **New computer? Restore with a card you used before**.
2. Enter any card code this account has used and the account number. Your points and usage come back, and your other computer keeps working.
3. One account works on up to 3 computers. If you reach the limit, go to **Settings** > **My computers** on any of them and **Disable** one you no longer use.
4. If a computer is lost or someone else has your card code, disable that computer from another one in **My computers**. It is cut off at once.

## Updates

The assistant checks for a new version when it opens and every 6 hours after that. When one is ready, your little dragon tells you at the top of the home page: choose **Restart to update**. It installs once running requests finish and reopens by itself. Open Claude Code and Codex windows keep working.

## Uninstalling

Uninstall ZilongAI Assistant from **Settings** > **Apps** in Windows. Claude Code and Codex go back to their previous settings automatically.

## Usage rules

The following are prohibited:

- Distillation: collecting model outputs in bulk to train or fine-tune other models.
- Jailbreaking: using prompts or other means to bypass a model's safety limits.
- Anything else that breaks the model providers' usage policies.

Accounts found doing this are permanently banned and points are not refunded. Continuing to use the service means you accept these rules.

## Refunds

Contact the seller of your card. Points are not refunded on accounts banned for breaking the usage rules.

## Troubleshooting

| What you see | What to do |
|---|---|
| Cannot reach the service | This is usually a network problem: turn off your proxy or switch nodes. Your account may already be open on the server, so when your network is back, choose **Activate** again on this computer to get in and see your account number. Still stuck? Choose **Contact support** on the activation page. |
| That card code is not right | Check for missing or extra characters. |
| This computer was signed in to ZilongAI before | A previous sign-in is still on this computer, even after a reinstall. If it is yours, choose **Keep using this account**. If it is not yours or you are unsure, choose **Not mine, enter a new card**. Nothing is taken over until you choose. |
| This card code has been used | If this is your own account, choose **New computer? Restore with a card you used before** and enter the account number. If you just activated on this computer and never saw an account number, the account is already open: choose **Activate** again. Still stuck? Choose **Contact support**. Support can give you the account number so you can restore it, and your points are safe. |
| This card code has expired | Card codes must be redeemed within 12 months of issue. Contact the seller. |
| This account already has 3 computers | Disable one in **My computers** on any of them. If none is at hand, contact support. |
| The request was blocked by the network | Turn off your proxy or switch nodes, then try again. |
| Codex shows `502 Bad Gateway: Unknown error` at address 127.0.0.1 | A proxy, VPN or antivirus HTTPS scan on your PC is usually in the way. Turn it off, then choose **Restart app**. If you cannot turn it off, contact support. |
| You used cc-switch or a similar tool to point Codex or Claude Code elsewhere (such as DeepSeek), and there is no model list after takeover | The assistant removes the model list and model names those tools left behind and restarts the app automatically. If it still looks wrong, choose **Restart app** on the **Overview** page or quit the app fully and reopen it. If those tools are still running, quit them first. |
| Claude Code or Codex is not using ZilongAI | If the **Overview** page shows a notice, choose **Restart app** or **Restart terminals**, or close and reopen the program yourself. Then choose **Run checkup**. If it warns about conflicting environment variables, remove or comment them out as it says and reopen your terminal. |
| Download failed, or The official download was refused, during a one-click install | Check your network, turn off your proxy or switch nodes, and try again. For a desktop app, you can also choose **Open download page** and install it yourself. In mainland China, the Codex CLI switches to a mirror in China automatically; Claude Code and the Claude app may not download, so contact support. |
| One-click install opened the Microsoft Store | The Codex app is only in the Microsoft Store, listed as ChatGPT. Choose **Get**, then come back and choose **Open app**. If the Store cannot install it, choose **Install CLI** to use the command-line version instead. |
| It says installed, but the assistant still shows it as missing | Open that app once from the Start menu, or quit and reopen the assistant. |
| Image generation says `ZilongAI Assistant is not running` | Open the assistant and try again. If it is already open, quit and reopen it. |
| Image generation says you are out of points or your points expired | Top up and try again. |
| You ask for an image and it says it needs an OpenAI key, has no image tool, or cannot switch because of a rule | Start a new conversation and ask again, because older conversations cannot see the new image settings. If it still happens, restart the app or terminal window from the assistant. |
| You ask for a song and it says it only has the image tool, or no music tool | This conversation was opened before the update. Close it and start a new one. If that does not help, quit and reopen the assistant. |
| It says a song is already being made | Each account can make 1 at a time. Wait for it to finish before starting the next one. |
| It says you have used today's songs | The limit is 5 a day. Try again after midnight China time. |
| It says music needs a regular card | Test cards cannot make music. It works as soon as you redeem a regular card. |
| A song will not open or has no sound | The file is an `.m4a` using the Opus codec, which a few older players do not support. Try VLC. |
| Your points expired | Top up during the 7-day freeze and all your points come back. |
| You forgot your account number | It is at the bottom of the sidebar and in **Settings** on your old computer. If that computer is gone, contact support. |

## Contact support

- Choose **Contact support** in the assistant to leave a message, even before activation. You get a notification when support replies. The **Messages** page also lists other ways to reach us.
- To get help faster, include the result of **Copy diagnostics** from **Settings**. It contains no tokens or keys.
