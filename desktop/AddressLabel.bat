
:: this file is for windows users to run the gui from the desktop environment
:: replace the cd argument with the absolute path you cloned this repo to
:: copy this file or make a shortcut and put it in ~\Desktop or '~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs'
:: you can change the icon of a shortcut to the icon in this repo

@echo off
cd /d "C:\the-path-of-this-repo-here"
uv run gui.py
