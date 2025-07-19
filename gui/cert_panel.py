# gui/cert_panel.py
import tkinter as tk
from tkinter import ttk
from cli.revoke import revoke_cert, unrevoke_cert

def load_cert_panel(parent):
    label = ttk.Label(parent, text="Enter Certificate Serial (hex):")
    label.pack(pady=10)

    entry = ttk.Entry(parent, width=60)
    entry.pack(pady=5)

    def revoke():
        serial = entry.get()
        print(f"🔴 Revoke clicked: {serial}")
        revoke_cert(serial)

    def unrevoke():
        serial = entry.get()
        print(f"🟢 Unrevoke clicked: {serial}")
        unrevoke_cert(serial)

    ttk.Button(parent, text="Revoke", command=revoke).pack(pady=10)
    ttk.Button(parent, text="Unrevoke", command=unrevoke).pack()
