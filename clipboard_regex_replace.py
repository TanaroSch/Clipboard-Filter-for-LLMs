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

# Set up logging
logging.basicConfig(filename='clipboard_regex_replace.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {str(e)}")
        return []


def replace_clipboard_text():
    try:
        # Get the current clipboard content
        text = pyperclip.paste()
        logging.info(f"Original text: {text}")

        # Load the config
        replacements = load_config()

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


def setup_keyboard():
    try:
        keyboard.add_hotkey('ctrl+alt+v', replace_clipboard_text)
        logging.info("Hotkey registered successfully")
    except Exception as e:
        logging.error(f"Failed to register hotkey: {str(e)}")
        logging.error(traceback.format_exc())


def run_script():
    setup_keyboard()
    logging.info("Script is running in the background.")


# Create a simple menu
menu = Menu(MenuItem('Exit', exit_action))

# Create a system tray icon
image = Image.new('RGB', (64, 64), color=(255, 0, 0))
icon = Icon("Clipboard Regex Replace", image, "Clipboard Regex Replace", menu)

# Run the script in a separate thread
script_thread = threading.Thread(target=run_script)
script_thread.start()

# Run the system tray icon
icon.run()

# When the icon is stopped, also stop the keyboard listener
keyboard.unhook_all()
