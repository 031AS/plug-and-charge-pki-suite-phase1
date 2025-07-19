import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_trust_chain(frame):
    G = nx.DiGraph()
    G.add_node("Root CA")
    G.add_node("Sub-CA EV")
    G.add_node("Sub-CA EVSE")
    G.add_node("EVCC Cert")
    G.add_node("SECC Cert")

    G.add_edges_from([
        ("Root CA", "Sub-CA EV"),
        ("Root CA", "Sub-CA EVSE"),
        ("Sub-CA EV", "EVCC Cert"),
        ("Sub-CA EVSE", "SECC Cert"),
    ])

    pos = nx.spring_layout(G)
    fig, ax = plt.subplots(figsize=(6, 4))
    nx.draw(G, pos, with_labels=True, arrows=True, node_size=3000,
            node_color='lightblue', font_size=9, ax=ax)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
