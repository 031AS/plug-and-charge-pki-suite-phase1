# gui/cert_panel.py
import tkinter as tk
from tkinter import ttk
from cli.revoke import revoke_cert, unrevoke_cert

def load_cert_panel(parent):
    label = ttk.Label(parent, text="Enter Certificate Serial (hex):")
    label.pack(pady=10)

    entry = ttk.Entry(parent, width=60)
    entry.pack(pady=5)

    # Status message label
    status_label = ttk.Label(parent, text="", foreground="blue")
    status_label.pack(pady=10)

    def revoke():
        serial = entry.get()
        if serial:
            revoke_cert(serial)
            status_label.config(text=f"🔴 Certificate {serial} revoked")

    def unrevoke():
        serial = entry.get()
        if serial:
            unrevoke_cert(serial)
            status_label.config(text=f"🟢 Certificate {serial} set to GOOD")

    ttk.Button(parent, text="Revoke", command=revoke).pack(pady=10)
    ttk.Button(parent, text="Unrevoke", command=unrevoke).pack()
