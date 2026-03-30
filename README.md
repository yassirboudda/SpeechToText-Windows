# SpeechToText — Windows

Voxtral-powered speech-to-text that lives in your Windows system tray.

Record speech, get instant transcription via Mistral's Voxtral API, and have it automatically typed at your cursor or copied to clipboard.

## Features

- **System tray app** — lives in the Windows notification area
- **Record & transcribe** — one click to record, auto-transcribes when you stop
- **Auto type at cursor** — transcription is automatically pasted where your cursor is (configurable)
- **Auto copy to clipboard** — transcription is always copied to clipboard
- **Visual editor** — optional floating editor to view/edit transcription
- **API key management** — add/test/manage your Mistral API key from Settings
- **2-minute recording limit** — optimized for Mistral's free tier

## Requirements

- Windows 10/11
- Python 3.9+
- A [Mistral API key](https://console.mistral.ai/)

## Installation

```powershell
# Clone the repo
git clone https://github.com/bouddahami/SpeechToText-Windows.git
cd SpeechToText-Windows

# Install dependencies
pip install -r requirements.txt

# Install the app
pip install .
```

## Usage

```powershell
speechtotext
```

Or run directly:

```powershell
python -m speechtotext
```

On first launch, you'll see only "🔑 Add API Key" in the tray menu. Click it to enter and test your Mistral API key.

## Auto-start on Login

### Option 1: Startup Folder

1. Press `Win+R`, type `shell:startup`, press Enter
2. Create a shortcut to `speechtotext.exe` (usually in `%LOCALAPPDATA%\Programs\Python\PythonXX\Scripts\`)

### Option 2: Registry

```powershell
# Find the path
where speechtotext

# Add to startup (replace path as needed)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v SpeechToText /t REG_SZ /d "C:\Users\YOU\AppData\Local\Programs\Python\Python312\Scripts\speechtotext.exe" /f
```

## Configuration

Config is stored at `%APPDATA%\SpeechToText\config.json`.

## Other Platforms

- [Linux version](https://github.com/bouddahami/SpeechToText)
- [macOS version](https://github.com/bouddahami/SpeechToText-macOS)
