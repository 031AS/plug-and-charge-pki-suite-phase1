# main.py
import sys
import os

# Ensure current root path is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import run_gui
from cli.revoke import run_revoke_cli

def main():
    mode = os.environ.get("MODE", "gui")
    if mode == "cli":
        run_revoke_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()

