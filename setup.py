import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame", "pygame_gui"],
    "include_files": ["config.xml", "assets/background.jpg"],   # Include config.xml in the build
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Set base to hide the console if desired, otherwise set to None

executables = [
    Executable(
        "main.py",  # Main script
        base=base,  # Set base to hide console
        icon=None,  # Optional: add path to .ico file if you have one
    )
]

setup(
    name="YourAppName",  # Name of your application
    version="1.0",
    description="Description of your app",
    options={"build_exe": build_exe_options},
    executables=executables
)
