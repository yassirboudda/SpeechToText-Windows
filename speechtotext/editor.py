"""Visual editor window using tkinter (Windows)."""

import tkinter as tk


def copy_to_clipboard(text):
    """Copy text to Windows clipboard via tkinter."""
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()


def show_editor(app):
    """Show the visual editor window."""
    win = tk.Tk()
    win.title('SpeechToText — Editor')
    win.geometry('420x400')
    win.resizable(True, True)
    win.configure(bg='#1e1e2e')
    win.attributes('-topmost', True)
    win.lift()

    # ── Header ──
    tk.Label(win, text='🎤  Transcription Editor', font=('Segoe UI', 14, 'bold'),
             bg='#1e1e2e', fg='#cdd6f4').pack(pady=(16, 8))

    # ── Text area ──
    text_frame = tk.Frame(win, bg='#313244', bd=1)
    text_frame.pack(fill='both', expand=True, padx=20, pady=(0, 6))

    text_widget = tk.Text(text_frame, wrap='word', font=('Segoe UI', 12),
                          bg='#181825', fg='#cdd6f4', insertbackground='#cdd6f4',
                          relief='flat', bd=8, undo=True)
    text_widget.pack(fill='both', expand=True)
    text_widget.insert('1.0', app.transcription or '')

    scrollbar = tk.Scrollbar(text_widget, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    def sync_back(*args):
        text = text_widget.get('1.0', 'end-1c').strip()
        app.update_transcription_from_editor(text)

    text_widget.bind('<<Modified>>', lambda e: (sync_back(), text_widget.edit_modified(False)))

    # ── Status ──
    status_var = tk.StringVar(value='Edit transcription text above')
    tk.Label(win, textvariable=status_var, font=('Segoe UI', 9),
             bg='#1e1e2e', fg='#6c7086', anchor='w').pack(fill='x', padx=20)

    # ── Buttons ──
    btn_frame = tk.Frame(win, bg='#1e1e2e')
    btn_frame.pack(fill='x', padx=20, pady=(6, 16))

    def on_copy():
        text = text_widget.get('1.0', 'end-1c').strip()
        if text:
            copy_to_clipboard(text)
            status_var.set('Copied to clipboard!')
        else:
            status_var.set('Nothing to copy')

    def on_type():
        text = text_widget.get('1.0', 'end-1c').strip()
        if not text:
            status_var.set('Nothing to type')
            return
        copy_to_clipboard(text)
        win.withdraw()
        win.after(700, _paste_and_show)

    def _paste_and_show():
        import pyautogui
        pyautogui.hotkey('ctrl', 'v')

    def on_delete():
        text_widget.delete('1.0', 'end')
        app.update_transcription_from_editor('')
        status_var.set('Transcription deleted')

    tk.Button(btn_frame, text='📋 Copy', command=on_copy,
              bg='#313244', fg='#a78bfa', relief='flat', bd=4,
              font=('Segoe UI', 10, 'bold'), cursor='hand2').pack(side='left', expand=True, fill='x', padx=(0, 4))

    tk.Button(btn_frame, text='⌨ Type at Cursor', command=on_type,
              bg='#7c3aed', fg='white', relief='flat', bd=4,
              font=('Segoe UI', 10, 'bold'), cursor='hand2').pack(side='left', expand=True, fill='x', padx=4)

    tk.Button(btn_frame, text='🗑 Delete', command=on_delete,
              bg='#313244', fg='#ef4444', relief='flat', bd=4,
              font=('Segoe UI', 10, 'bold'), cursor='hand2').pack(side='left', expand=True, fill='x', padx=(4, 0))

    win.mainloop()
