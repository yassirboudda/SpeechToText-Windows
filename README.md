# SpeechToText — Windows

Voxtral-powered speech-to-text that lives in your Windows system tray.

Record speech, get instant transcription via Mistral's Voxtral API, and have it automatically typed at your cursor or copied to clipboard.

## Download & Install (No Python Required)

> **Go to the [Releases page](https://github.com/bouddahami/SpeechToText-Windows/releases/latest) and download:**

| File | Description |
|------|-------------|
| **`SpeechToText-Setup.exe`** | **Installer (recommended)** — installs to Program Files, creates Start Menu & Desktop shortcuts, optional auto-start on login |
| **`SpeechToText.exe`** | **Portable** — single file, no install needed, just double-click and run |

### Quick start

1. Download **`SpeechToText-Setup.exe`** and run it
2. The app appears in the **system tray** (bottom-right of your taskbar, near the clock)
3. Right-click the tray icon → **Add API Key**
4. Get a free API key from [console.mistral.ai](https://console.mistral.ai/) (create an account, go to API Keys)
5. Paste your key, click **Test Key**, then **Save**
6. Right-click the tray icon → **Start Recording** → speak → **Stop Recording**
7. Your transcription is automatically typed where your cursor is!

## Features

- **System tray app** — lives in the Windows notification area
- **Record & transcribe** — one click to record, auto-transcribes when you stop
- **Auto type at cursor** — transcription is automatically pasted where your cursor is (configurable)
- **Auto copy to clipboard** — transcription is always copied to clipboard
- **Visual editor** — optional floating editor to view/edit transcription
- **API key management** — add/test/manage your Mistral API key from Settings
- **2-minute recording limit** — optimized for Mistral's free tier

## Install from Source (for developers)

<details>
<summary>Click to expand developer instructions</summary>

### Requirements

- Windows 10/11
- Python 3.9+
- A [Mistral API key](https://console.mistral.ai/)

### Installation

```powershell
# Clone the repo
git clone https://github.com/bouddahami/SpeechToText-Windows.git
cd SpeechToText-Windows

# Install dependencies
pip install -r requirements.txt

# Install the app
pip install .
```

### Usage

```powershell
speechtotext
```

Or run directly:

```powershell
python -m speechtotext
```

### Build the .exe yourself

```powershell
pip install pyinstaller
build.bat
# Output: dist\SpeechToText.exe
```

</details>

## Auto-start on Login

If you used the **installer**, check the "Start when Windows starts" option during setup.

Otherwise:

1. Press `Win+R`, type `shell:startup`, press Enter
2. Copy `SpeechToText.exe` (or a shortcut to it) into that folder

## Configuration

Config is stored at `%APPDATA%\SpeechToText\config.json`.

## Other Platforms

- [Linux version](https://github.com/bouddahami/SpeechToText-Linux)
- [macOS version](https://github.com/bouddahami/SpeechToText-macOS)
