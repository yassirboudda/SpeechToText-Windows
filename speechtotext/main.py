#!/usr/bin/env python3
"""SpeechToText - Voxtral-powered speech transcription for Windows system tray."""

import sys
import json
import os
import threading
import time

from speechtotext.recorder import AudioRecorder
from speechtotext.transcriber import transcribe, test_api_key

CONFIG_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'SpeechToText')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

DEFAULT_CONFIG = {
    'mistral_api_key': '',
    'auto_type_at_cursor': True,
}


def load_config():
    """Load configuration from config file."""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return dict(DEFAULT_CONFIG)

    with open(CONFIG_FILE) as f:
        stored = json.load(f)
    config = dict(DEFAULT_CONFIG)
    config.update(stored)
    return config


def save_config(config):
    """Save configuration to config file."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def copy_to_clipboard(text):
    """Copy text to Windows clipboard via tkinter."""
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()


def paste_at_cursor():
    """Simulate Ctrl+V on Windows."""
    import pyautogui
    pyautogui.hotkey('ctrl', 'v')


def _create_tray_icon():
    """Create a simple tray icon image."""
    from PIL import Image, ImageDraw
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Purple circle with mic shape
    draw.ellipse([4, 4, 60, 60], fill='#7c3aed')
    draw.ellipse([22, 12, 42, 38], fill='white')
    draw.rectangle([28, 38, 36, 48], fill='white')
    draw.arc([20, 30, 44, 52], 0, 180, fill='white', width=3)
    return img


class SpeechToTextApp:
    """System tray speech-to-text app for Windows using pystray."""

    PREVIEW_LEN = 50

    def __init__(self, config):
        import pystray
        self.pystray = pystray
        self.config = config
        self.api_key = config.get('mistral_api_key', '')
        self.auto_type = config.get('auto_type_at_cursor', True)
        self.recorder = AudioRecorder()
        self.is_recording = False
        self.is_transcribing = False
        self.transcription = ''
        self.status_text = 'Ready'

        icon_image = _create_tray_icon()
        self.icon = pystray.Icon(
            'SpeechToText',
            icon_image,
            'SpeechToText',
            menu=self._build_menu(),
        )
        self.icon.run()

    def _build_menu(self):
        from pystray import MenuItem as Item, Menu

        if not self.api_key:
            return Menu(
                Item('🔑  Add API Key', self._on_settings),
                Menu.SEPARATOR,
                Item('Quit', self._on_quit),
            )

        return Menu(
            Item(lambda _: '⏹  Stop Recording' if self.is_recording else
                 ('⏳  Transcribing…' if self.is_transcribing else '🎙  Start Recording'),
                 self._on_record),
            Item(lambda _: self.status_text, None, enabled=False),
            Menu.SEPARATOR,
            Item(lambda _: self._get_preview(), None, enabled=False),
            Menu.SEPARATOR,
            Item('📋  Copy to Clipboard', self._on_copy,
                 enabled=lambda _: bool(self.transcription.strip())),
            Item('⌨  Type at Cursor', self._on_type,
                 enabled=lambda _: bool(self.transcription.strip())),
            Item('🗑  Delete Transcription', self._on_delete,
                 enabled=lambda _: bool(self.transcription.strip())),
            Menu.SEPARATOR,
            Item('📝  Visual Editor', self._on_editor),
            Item('⚙  Settings', self._on_settings),
            Menu.SEPARATOR,
            Item('Quit', self._on_quit),
        )

    def _get_preview(self):
        if self.transcription.strip():
            preview = self.transcription.replace('\n', ' ')
            if len(preview) > self.PREVIEW_LEN:
                preview = preview[:self.PREVIEW_LEN] + '…'
            return preview
        return 'No transcription yet'

    def _refresh(self):
        self.icon.update_menu()

    # ── Handlers ──

    def _on_record(self, icon, item):
        if self.is_transcribing:
            return
        if self.is_recording:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self):
        try:
            self.recorder.start(
                on_duration_update=self._on_tick,
                on_max_reached=self._on_max,
            )
            self.is_recording = True
            self.status_text = 'Recording…'
            self._refresh()
        except Exception as e:
            self.status_text = f'Error: {e}'
            self._refresh()

    def _stop_recording(self):
        filepath = self.recorder.stop()
        self.is_recording = False

        if filepath:
            self.is_transcribing = True
            self.status_text = 'Transcribing…'
            self._refresh()
            t = threading.Thread(target=self._transcribe_bg, args=(filepath,), daemon=True)
            t.start()
        else:
            self._refresh()

    def _on_tick(self, seconds):
        dur = self.recorder.format_duration(seconds)
        self.status_text = f'Recording… {dur}'
        self._refresh()

    def _on_max(self):
        self._stop_recording()

    def _transcribe_bg(self, filepath):
        try:
            text = transcribe(filepath, self.api_key)
            self._on_transcribe_ok(text)
        except Exception as e:
            self._on_transcribe_err(str(e))
        finally:
            self.recorder.cleanup()

    def _on_transcribe_ok(self, text):
        self.is_transcribing = False
        if text:
            if self.transcription.strip():
                self.transcription += '\n' + text
            else:
                self.transcription = text
            copy_to_clipboard(self.transcription.strip())
            if self.auto_type:
                self.status_text = '✓ Typing at cursor…'
                self._refresh()
                time.sleep(0.7)
                paste_at_cursor()
            else:
                self.status_text = '✓ Copied to clipboard – ready to paste'
        else:
            self.status_text = 'No speech detected'
        self._refresh()

    def _on_transcribe_err(self, error):
        self.is_transcribing = False
        self.status_text = f'Error: {error}'
        self._refresh()

    def _on_copy(self, icon, item):
        text = self.transcription.strip()
        if text:
            copy_to_clipboard(text)
            self.status_text = 'Copied to clipboard!'
            self._refresh()

    def _on_type(self, icon, item):
        text = self.transcription.strip()
        if not text:
            return
        copy_to_clipboard(text)
        threading.Thread(target=self._delayed_paste, daemon=True).start()

    def _delayed_paste(self):
        time.sleep(0.7)
        paste_at_cursor()

    def _on_delete(self, icon, item):
        self.transcription = ''
        self.status_text = 'Transcription deleted'
        self._refresh()

    def _on_editor(self, icon, item):
        threading.Thread(target=self._show_editor, daemon=True).start()

    def _show_editor(self):
        from speechtotext.editor import show_editor
        show_editor(self)

    def _on_settings(self, icon, item):
        threading.Thread(target=self._show_settings, daemon=True).start()

    def _show_settings(self):
        from speechtotext.settings import show_settings
        show_settings(self)

    def _on_quit(self, icon, item):
        self.icon.stop()

    def apply_settings(self, new_api_key, new_auto_type):
        """Apply changed settings."""
        self.api_key = new_api_key
        self.auto_type = new_auto_type
        self.config['mistral_api_key'] = new_api_key
        self.config['auto_type_at_cursor'] = new_auto_type
        save_config(self.config)
        self.icon.menu = self._build_menu()
        self._refresh()

    def update_transcription_from_editor(self, text):
        self.transcription = text
        self._refresh()


def main():
    """Main entry point."""
    config = load_config()
    SpeechToTextApp(config)


if __name__ == '__main__':
    main()
