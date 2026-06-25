# TracePathVisualizer (TPV)
# Copyright (c) 2026 NoF8
# Licensed under the MIT License

import ctypes

from app.cli import run_cli


# ==================================================
# Maximise Console Window
# ==================================================

def maximise_console() -> None:
    SW_MAXIMIZE = 3

    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, SW_MAXIMIZE)


# ==================================================
# Application Entry Point
# ==================================================

if __name__ == "__main__":
    maximise_console()
    run_cli()