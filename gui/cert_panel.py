# gui/cert_panel.py
import tkinter as tk
from tkinter import ttk
from cli.revoke import revoke_cert, unrevoke_cert

def load_cert_panel(frame):
    print("✅ load_cert_panel() called")  # Debug

    label = ttk.Label(frame, text="Enter Certificate Serial (hex):")
    label.pack(pady=10)

    serial_entry = ttk.Entry(frame, width=50)
    serial_entry.pack(pady=5)

    def handle_revoke():
        serial = serial_entry.get()
        print(f"🔴 Revoke clicked for serial: {serial}")
        if serial:
            revoke_cert(serial)

    def handle_unrevoke():
        serial = serial_entry.get()
        print(f"🟢 Unrevoke clicked for serial: {serial}")
        if serial:
            unrevoke_cert(serial)

    btn_revoke = ttk.Button(frame, text="Revoke", command=handle_revoke)
    btn_revoke.pack(pady=10)

    btn_unrevoke = ttk.Button(frame, text="Unrevoke", command=handle_unrevoke)
    btn_unrevoke.pack()
