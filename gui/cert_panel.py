import os
import tkinter as tk
from tkinter import messagebox
from pki.generate_evcc_csr import generate_evcc_csr

def load_cert_panel(parent, log_callback):
    panel = tk.Frame(parent)

    # ========== Section: Generate CSR ==========
    tk.Label(panel, text="Enter EMAID (e.g. DE*ABC*E1234567*1):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    emaid_entry = tk.Entry(panel, width=40)
    emaid_entry.grid(row=0, column=1, padx=5, pady=5)

    def on_generate_csr():
        emaid = emaid_entry.get().strip()
        if not emaid:
            messagebox.showerror("Missing EMAID", "Please enter a valid EMAID.")
            return
        try:
            key_path, csr_path = generate_evcc_csr(emaid)
            log_callback(f"✅ CSR generated!\n🔑 Key: {key_path}\n📄 CSR: {csr_path}")
        except Exception as e:
            log_callback(f"❌ Error generating CSR: {e}")

    gen_csr_btn = tk.Button(panel, text="Generate CSR", command=on_generate_csr, bg="#e0e0ff")
    gen_csr_btn.grid(row=1, column=0, columnspan=2, pady=10)

    return panel
