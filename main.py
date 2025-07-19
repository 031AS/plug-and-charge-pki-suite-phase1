# main.py
import os
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
