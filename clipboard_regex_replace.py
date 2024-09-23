import keyboard
import pyperclip
import re
import logging
import traceback
import json
from time import sleep
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import os
import sys

# Set up logging
logging.basicConfig(filename='clipboard_regex_replace.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {str(e)}")
        return {}


def get_clipboard_text():
    if sys.platform == 'win32':
        import win32clipboard
        win32clipboard.OpenClipboard()
        try:
            return win32clipboard.GetClipboardData()
        finally:
            win32clipboard.CloseClipboard()
    elif sys.platform == 'linux':
        import subprocess
        return subprocess.check_output(['xclip', '-selection', 'clipboard', '-o']).decode('utf-8')
    else:
        raise NotImplementedError("Unsupported platform")


def set_clipboard_text(text):
    if sys.platform == 'win32':
        import win32clipboard
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text)
        finally:
            win32clipboard.CloseClipboard()
    elif sys.platform == 'linux':
        import subprocess
        subprocess.run(['xclip', '-selection', 'clipboard'],
                       input=text.encode('utf-8'))
    else:
        raise NotImplementedError("Unsupported platform")


def simulate_paste():
    if sys.platform == 'win32':
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('^v')
    elif sys.platform == 'linux':
        import subprocess
        subprocess.run(['xdotool', 'key', 'ctrl+v'])
    else:
        raise NotImplementedError("Unsupported platform")


def show_notification(title, message):
    config = load_config()
    if config.get('use_notifications', False):
        try:
            from plyer import notification
            notification.notify(
                title=title,
                message=message,
                app_name='Clipboard Regex Replace',
                timeout=2  # Display for 2 seconds
            )
        except ImportError:
            logging.warning(
                "Plyer library not installed. Notifications disabled.")
        except Exception as e:
            logging.error(f"Failed to show notification: {str(e)}")


def replace_clipboard_text():
    try:
        # Get the current clipboard content
        text = pyperclip.paste()
        logging.info(f"Original text: {text}")

        # Load the config
        config = load_config()
        replacements = config.get('replacements', [])

        # Apply all regex replacements
        for replacement in replacements:
            pattern = replacement['regex']
            replace_with = replacement['replace_with']
            text = re.sub(pattern, replace_with, text, flags=re.UNICODE)

        logging.info(f"Modified text: {text}")

        # Set the new text to clipboard
        pyperclip.copy(text)

        # Show notification
        show_notification(
            "Clipboard Updated", "Text has been replaced according to your regex rules.")

        # Wait to ensure the clipboard is updated
        sleep(0.5)

        # Attempt to paste
        try:
            if sys.platform == 'win32':
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('^v')
            elif sys.platform == 'linux':
                import subprocess
                subprocess.run(['xdotool', 'key', 'ctrl+v'])
            else:
                raise NotImplementedError("Unsupported platform")
            logging.info("Automatic paste attempted")
        except Exception as paste_error:
            logging.error(f"Automatic paste failed: {str(paste_error)}")
            logging.info(
                "Automatic paste failed. Please press Ctrl+V to paste manually.")
            show_notification(
                "Paste Failed", "Please press Ctrl+V to paste manually.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        logging.error(traceback.format_exc())


def exit_action(icon):
    icon.stop()


def setup_keyboard(hotkey):
    try:
        keyboard.add_hotkey(hotkey, replace_clipboard_text)
        logging.info(f"Hotkey {hotkey} registered successfully")
    except Exception as e:
        logging.error(f"Failed to register hotkey: {str(e)}")
        logging.error(traceback.format_exc())


def run_script(hotkey):
    setup_keyboard(hotkey)
    logging.info("Script is running in the background.")


def load_icon(icon_path):
    if icon_path and os.path.exists(icon_path):
        try:
            return Image.open(icon_path)
        except Exception as e:
            logging.error(f"Failed to load icon: {str(e)}")

    # Default to red square if icon_path is not provided or invalid
    return Image.new('RGB', (64, 64), color=(255, 0, 0))


def main():
    config = load_config()
    hotkey = config.get('hotkey', 'ctrl+alt+v')
    icon_path = config.get('icon_path')

    # Create a simple menu
    menu = Menu(MenuItem('Exit', exit_action))

    # Load icon
    image = load_icon(icon_path)

    # Create a system tray icon
    icon = Icon("Clipboard Regex Replace", image,
                "Clipboard Regex Replace", menu)

    # Run the script in a separate thread
    script_thread = threading.Thread(target=run_script, args=(hotkey,))
    script_thread.start()

    # Run the system tray icon
    icon.run()

    # When the icon is stopped, also stop the keyboard listener
    keyboard.unhook_all()


if __name__ == "__main__":
    main()
