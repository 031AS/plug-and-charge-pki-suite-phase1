# gui/app.py
import tkinter as tk
from tkinter import ttk
from gui.trust_visualizer import draw_trust_chain
from gui.cert_panel import load_cert_panel
from tls.handshake_simulator import simulate_tls_handshake

def run_gui():
    root = tk.Tk()
    root.title("031AS Plug & Charge PKI Suite")
    root.geometry("900x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    frame3 = ttk.Frame(notebook)

    notebook.add(frame1, text="Trust Chain")
    notebook.add(frame2, text="Certificate Manager")
    notebook.add(frame3, text="TLS Simulation")

    for f in (frame1, frame2, frame3):
        f.pack(fill="both", expand=True)

    draw_trust_chain(frame1)
    load_cert_panel(frame2)

    ttk.Button(
        frame3,
        text="Run Handshake",
        command=lambda: simulate_tls_handshake(
            "certificates/secc1.pem",
            "certificates/secc1.key",
            "certificates/root_ca.pem"
        )
    ).pack(pady=40)

    root.mainloop()
