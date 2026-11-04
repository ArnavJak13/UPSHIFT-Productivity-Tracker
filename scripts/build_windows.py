"""Optional helper to build a Windows executable using PyInstaller.

Run this only after the project is finished and tested.
"""

import subprocess


command = [
    "pyinstaller",
    "--noconfirm",
    "--windowed",
    "--name",
    "UPSHIFT",
    "main.py"
]

print("Building UPSHIFT...")
subprocess.run(command)
print("Finished. Check the dist folder.")
