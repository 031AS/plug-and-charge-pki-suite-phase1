# gui/cert_panel.py

import tkinter as tk
from tkinter import messagebox
import json
import os

from tls.handshake_runner import run_tls_handshake_gui

DB_PATH = "cert_db.json"

def load_cert_panel(frame):
    print("✅ load_cert_panel() called")

    label = tk.Label(frame, text="Enter Certificate Serial (hex):", font=("Arial", 10))
    label.pack(pady=5)

    serial_entry = tk.Entry(frame, width=50)
    serial_entry.pack(pady=5)

    def save_status(serial, status):
        if not os.path.exists(DB_PATH):
            db = {}
        else:
            with open(DB_PATH, "r") as f:
                db = json.load(f)

        db[serial] = status

        with open(DB_PATH, "w") as f:
            json.dump(db, f, indent=4)

    def revoke_cert():
        serial = serial_entry.get().strip().lower()
        if serial:
            print(f"🔴 Revoke clicked: {serial}")
            save_status(serial, "revoked")
            print(f"🔴 Certificate {serial} marked as REVOKED.")
        else:
            messagebox.showwarning("Input Error", "Please enter a serial number.")

    def unrevoke_cert():
        serial = serial_entry.get().strip().lower()
        if serial:
            print(f"🟢 Unrevoke clicked: {serial}")
            save_status(serial, "good")
            print(f"🟢 Certificate {serial} restored to GOOD.")
        else:
            messagebox.showwarning("Input Error", "Please enter a serial number.")

    revoke_button = tk.Button(frame, text="Revoke", command=revoke_cert)
    revoke_button.pack(pady=2)

    unrevoke_button = tk.Button(frame, text="Unrevoke", command=unrevoke_cert)
    unrevoke_button.pack(pady=2)

    # TLS Handshake button
    tls_button = tk.Button(frame, text="Run Handshake", command=run_tls_handshake_gui)
    tls_button.pack(pady=10)

