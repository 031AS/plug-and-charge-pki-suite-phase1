# gui/app.py
import tkinter as tk
from tkinter import ttk
from gui.trust_visualizer import draw_trust_chain
from gui.cert_panel import load_cert_panel
from tls.handshake_simulator import simulate_tls_handshake

def run_gui():
    root = tk.Tk()
    root.title("031AS Plug & Charge PKI Suite")
    root.geometry("700x500")  # 👈 optional, ensures space for tabs

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    # Create the frames
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    frame3 = ttk.Frame(notebook)

    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    frame3.pack(fill='both', expand=True)

    # Add tabs
    notebook.add(frame1, text="Trust Chain")
    notebook.add(frame2, text="Certificate Manager")
    notebook.add(frame3, text="TLS Simulation")

    # Load tab contents
    # draw_trust_chain(frame1)
    load_cert_panel(frame2)

    btn = ttk.Button(frame3, text="Run Handshake", command=lambda: simulate_tls_handshake(
        "certificates/secc1.pem",
        "certificates/secc1.key",
        "certificates/root_ca.pem"
    ))
    btn.pack(pady=40)

    root.mainloop()
