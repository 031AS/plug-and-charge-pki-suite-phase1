# gui/cert_panel.py
import tkinter as tk
from tkinter import ttk
from cli.revoke import revoke_cert, unrevoke_cert

def load_cert_panel(parent):
    container = ttk.Frame(parent)
    container.pack(fill='both', expand=True, padx=20, pady=20)

    label = ttk.Label(container, text="Enter Certificate Serial (hex):")
    label.pack(pady=(0, 10))

    serial_entry = ttk.Entry(container, width=60)
    serial_entry.pack(pady=5)

    def handle_revoke():
        serial = serial_entry.get()
        if serial:
            revoke_cert(serial)

    def handle_unrevoke():
        serial = serial_entry.get()
        if serial:
            unrevoke_cert(serial)

    btn_frame = ttk.Frame(container)
    btn_frame.pack(pady=15)

    btn_revoke = ttk.Button(btn_frame, text="Revoke", command=handle_revoke)
    btn_unrevoke = ttk.Button(btn_frame, text="Unrevoke", command=handle_unrevoke)

    btn_revoke.grid(row=0, column=0, padx=10)
    btn_unrevoke.grid(row=0, column=1, padx=10)
