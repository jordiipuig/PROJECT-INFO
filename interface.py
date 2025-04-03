import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Variables globales
current_graph = None
canvas = None
fig = None
ax = None
selected_nodes = []
modo = "navegar"  # modos: "nodo", "segmento", "vecinos"

# Ventana principal
root = tk.Tk()
root.title("Interfaz de Grafos")
root.geometry("700x700")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

frame_plot = tk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True)

def set_modo(nuevo_modo):
    global modo, selected_nodes
    modo = nuevo_modo
    selected_nodes.clear()
    messagebox.showinfo("Modo activado", f"Modo '{modo}' activado.\nHaz clic sobre el grafo.")

def plot_interactive_graph(g):
    global fig, ax, canvas, selected_nodes, current_graph
    selected_nodes = []

    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots()
    ax.set_title(f"Modo activo: {modo.upper()}")
    ax.grid(True, color='red', linestyle='--')

    for node in g.nodes:
        ax.plot(node.x, node.y, 'o', color='gray')
        ax.text(node.x + 0.2, node.y + 0.2, node.name)

    for segment in g.segments:
        x = [segment.origin.x, segment.destination.x]
        y = [segment.origin.y, segment.destination.y]
        ax.plot(x, y, 'b-')
        mx = (x[0] + x[1]) / 2
        my = (y[0] + y[1]) / 2
        ax.text(mx, my, f"{segment.cost:.2f}", color='blue', fontsize=8)

    def find_closest_node(x, y):
        return min(g.nodes, key=lambda n: ((n.x - x) ** 2 + (n.y - y) ** 2) ** 0.5)

    def on_click(event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata

        if modo == "nodo":
            name = simpledialog.askstring("Nuevo nodo", "Nombre del nodo:")
            if name:
                AddNode(current_graph, Node(name, x, y))
                plot_interactive_graph(current_graph)

        elif modo == "segmento":
            closest = find_closest_node(x, y)
            selected_nodes.append(closest)
            if len(selected_nodes) == 2:
                name = simpledialog.askstring("Nombre del segmento", "Introduce nombre del segmento:")
                if name:
                    AddSegment(current_graph, name, selected_nodes[0].name, selected_nodes[1].name)
                selected_nodes.clear()
                plot_interactive_graph(current_graph)

        elif modo == "vecinos":
            closest = find_closest_node(x, y)
            plot_neighbors(current_graph, closest)

        elif event.button == 3:  # clic derecho
            closest = find_closest_node(x, y)
            if messagebox.askyesno("Eliminar nodo", f"¿Eliminar nodo '{closest.name}'?"):
                RemoveNode(current_graph, closest.name)
                plot_interactive_graph(current_graph)

    fig.canvas.mpl_connect("button_press_event", on_click)

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

def plot_neighbors(g, node):
    global fig, ax, canvas

    if canvas:
        canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots()
    ax.set_title(f"Vecinos de {node.name}")
    ax.grid(True, color='red', linestyle='--')

    for n in g.nodes:
        color = 'gray'
        if n == node:
            color = 'blue'
        elif n in node.neighbors:
            color = 'green'
        ax.plot(n.x, n.y, 'o', color=color)
        ax.text(n.x + 0.2, n.y + 0.2, n.name)

    for segment in g.segments:
        if segment.origin == node and segment.destination in node.neighbors:
            x = [segment.origin.x, segment.destination.x]
            y = [segment.origin.y, segment.destination.y]
            ax.plot(x, y, 'r-')
            mx = (x[0] + x[1]) / 2
            my = (y[0] + y[1]) / 2
            ax.text(mx, my, f"{segment.cost:.2f}", color='red', fontsize=8)
        else:
            x = [segment.origin.x, segment.destination.x]
            y = [segment.origin.y, segment.destination.y]
            ax.plot(x, y, 'b-', alpha=0.2)

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

def load_graph_from_file():
    global current_graph
    path = filedialog.askopenfilename()
    if path:
        current_graph = LoadGraphFromFile(path)
        plot_interactive_graph(current_graph)

def load_example_graph():
    global current_graph
    current_graph = CreateGraph_1()
    plot_interactive_graph(current_graph)

def load_graph_2():
    global current_graph
    current_graph = CreateGraph_2()
    plot_interactive_graph(current_graph)

def nuevo_grafo():
    global current_graph
    current_graph = Graph()
    plot_interactive_graph(current_graph)

def guardar_grafo():
    global current_graph
    if not current_graph:
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        SaveGraphToFile(current_graph, path)
        messagebox.showinfo("Éxito", "Grafo guardado correctamente.")

# Botones principales
tk.Button(frame_buttons, text="Cargar Grafo desde Archivo", command=load_graph_from_file, width=30).pack(pady=5)
tk.Button(frame_buttons, text="Mostrar Grafo Ejemplo", command=load_example_graph, width=30).pack(pady=5)
tk.Button(frame_buttons, text="Mostrar Mi Grafo (graph_data.txt)", command=load_graph_2, width=30).pack(pady=5)
tk.Button(frame_buttons, text="Nuevo Grafo (Vacío)", command=nuevo_grafo, width=30).pack(pady=5)
tk.Button(frame_buttons, text="Guardar Grafo en Archivo", command=guardar_grafo, width=30).pack(pady=5)

# Modos interactivos
tk.Label(frame_buttons, text="Modo de clic:").pack(pady=(10,0))
tk.Button(frame_buttons, text="➕ Añadir Nodo", command=lambda: set_modo("nodo"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🔗 Añadir Segmento", command=lambda: set_modo("segmento"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="👁️ Ver Vecinos", command=lambda: set_modo("vecinos"), width=30).pack(pady=2)

# Iniciar interfaz
root.mainloop()
