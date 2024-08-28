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

        # Wait a bit to ensure the clipboard is updated
        sleep(0.1)

        # Simulate Ctrl+V to paste the new text
        keyboard.press_and_release('ctrl+v')

        logging.info("Text replacement and paste successful")
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
