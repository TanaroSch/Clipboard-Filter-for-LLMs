# Clipboard Regex Replace

Clipboard Regex Replace is a lightweight application that allows you to automatically apply regex-based replacements to your clipboard content using a customizable hotkey. The application is currently only tested on Windows, but might also work on Linux and Mac.

This application can be used to obfuscate names, personal data or directories from content pasted to LLMs automatically.

## Features

- Apply multiple regex replacements to clipboard content
- Customizable keyboard shortcut
- System tray icon for easy access and management
- Configurable via a JSON file
- Custom icon support

## Requirements

- Python 3.6+

### Conda Environment (optional)

```
conda create -y -n clipboard_regex_env
conda activate clipboard_regex_env
```

## Installation

1. Clone this repository or download the source code.
2. Install the required Python packages:

```
pip install keyboard pyperclip pystray pillow
```

3. Copy the `config.json.example` file to `config.json` and modify it according to your needs.

## Configuration

The `config.json` file allows you to customize the behavior of the application. Here's an example configuration:

```json
{
  "hotkey": "ctrl+alt+v",
  "icon_path": "path/to/your/icon.png",
  "replacements": [
    {
      "regex": "(?i)name[s]?[/\\\\]?",
      "replace_with": ""
    },
    {
      "regex": "example_pattern",
      "replace_with": "example_replacement"
    }
  ]
}
```

- `hotkey`: The keyboard shortcut to trigger the replacement (default: "ctrl+alt+v")
- `icon_path`: Path to a custom icon file (PNG format recommended)
- `replacements`: An array of regex replacement rules
  - `regex`: The regex pattern to match
  - `replace_with`: The string to replace the matched pattern with

## Usage

1. Run the `clipboard_regex_replace.py` script:

```
python clipboard_regex_replace.py
```

2. The application will start and show an icon in the system tray.
3. Copy some text to your clipboard.
4. Press the configured hotkey (default: Ctrl+Alt+V).
5. The application will apply all configured regex replacements to the clipboard content and automatically paste the result.

## Running at Startup

### Windows

1. Create a shortcut to the `StartClipboard.bat` file.
2. Press Win+R, type `shell:startup`, and press Enter.
3. Move the created shortcut to the Startup folder that opens.

## Logging

The application logs its activities to `clipboard_regex_replace.log` in the same directory as the script. Check this file if you encounter any issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.