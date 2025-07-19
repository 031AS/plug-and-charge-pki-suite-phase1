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

    csr_btn = tk.Button(panel, text="Generate CSR", command=on_generate_csr, bg="#e0e0ff")
    csr_btn.grid(row=1, column=0, columnspan=2, pady=5)

    # ========== Section: Generate SECC Chain ==========
    def generate_secc_chain():
        subca_path = "certificates/subca_secc.pem"
        root_path = "certificates/root_ca.pem"
        chain_path = "certificates/chain_secc.pem"

        if not os.path.exists(subca_path) or not os.path.exists(root_path):
            log_callback("❌ Missing SECC Sub-CA or Root CA files.")
            return

        try:
            with open(chain_path, "wb") as out:
                for p in [subca_path, root_path]:
                    with open(p, "rb") as f:
                        out.write(f.read())

            log_callback(f"✅ SECC chain written to: {chain_path}")
        except Exception as e:
            log_callback(f"❌ Failed to generate SECC chain: {e}")

    secc_btn = tk.Button(panel, text="Generate SECC Chain", command=generate_secc_chain, bg="#ffeecc")
    secc_btn.grid(row=2, column=0, columnspan=2, pady=5)

    return panel

