@echo off
setlocal enabledelayedexpansion

:: Get the directory of the batch file
set "SCRIPT_DIR=%~dp0"

call conda activate clipboard_regex_env

:: Run the Python script
start /B pythonw "!SCRIPT_DIR!clipboard_regex_replace.py"