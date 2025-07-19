import tkinter as tk
from gui.cert_panel import load_cert_panel
from gui.trust_visualizer import update_trust_graph
from tls.evcc_client import run_evcc_tls
from cli.revoke import run_revoke_cli

def run_gui():
    root = tk.Tk()
    root.title("031AS Plug & Charge Suite")
    root.geometry("800x600")

    # ========== Notebook Tabs ==========
    from tkinter import ttk
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Frames for tabs
    frame1 = tk.Frame(notebook)
    frame2 = tk.Frame(notebook)
    frame3 = tk.Frame(notebook)
    frame4 = tk.Frame(notebook)

    notebook.add(frame1, text="Trust Chain")
    notebook.add(frame2, text="Cert Management")
    notebook.add(frame3, text="TLS Simulation")
    notebook.add(frame4, text="Revocation")

    # ========== Frame 1: Trust Chain ==========
    tk.Button(frame1, text="Update Trust Graph", command=update_trust_graph).pack(pady=20)

    # ========== Frame 2: Certificate Panel ==========
    log_output = tk.Text(frame2, height=20, width=90)
    log_output.pack(pady=10)

    def log(msg):
        log_output.insert(tk.END, msg + "\n")
        log_output.see(tk.END)

    cert_panel = load_cert_panel(frame2, log)
    cert_panel.pack()

    # ========== Frame 3: TLS Simulation ==========
    def run_handshake():
        result = run_evcc_tls()
        log(f"{result}")

    tk.Button(frame3, text="Run TLS Handshake", command=run_handshake, bg="#ccffcc").pack(pady=40)

    # ========== Frame 4: CLI Revoke ==========
    tk.Button(frame4, text="Open Revoke CLI", command=run_revoke_cli).pack(pady=40)

    root.mainloop()
