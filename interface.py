import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from graph import *
from graph import FindShortestPath
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

current_graph = None
canvas = None
fig = None
ax = None
selected_nodes = []
modo = "navegar"

root = tk.Tk()
root.title("Gestor Visual de Grafos")
root.geometry("900x800")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

frame_plot = tk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True)

def set_modo(nuevo_modo):
    global modo, selected_nodes
    modo = nuevo_modo
    selected_nodes.clear()
    messagebox.showinfo("Modo activado", f"Modo '{modo}' activado.\nHaz clic sobre el grafo.")

def find_closest_node(x, y):
    if not current_graph or not current_graph.nodes:
        return None
    return min(current_graph.nodes, key=lambda n: ((n.x - x)**2 + (n.y - y)**2)**0.5)

def plot_graph(g):
    global fig, ax, canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    fig, ax = plt.subplots()
    ax.set_title("Grafo Actual")
    ax.grid(True, linestyle='--', color='lightgray')
    for seg in g.segments:
        x = [seg.origin.x, seg.destination.x]
        y = [seg.origin.y, seg.destination.y]
        ax.plot(x, y, 'gray')
        mx = (x[0] + x[1]) / 2
        my = (y[0] + y[1]) / 2
        ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8)
    for n in g.nodes:
        ax.plot(n.x, n.y, 'o', color='steelblue')
        ax.text(n.x + 0.2, n.y + 0.2, n.name, fontsize=9)
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()
    fig.canvas.mpl_connect("button_press_event", on_click)

def on_click(event):
    global modo, selected_nodes
    if not event.inaxes or current_graph is None:
        return
    x, y = event.xdata, event.ydata

    if modo == "nodo":
        name = simpledialog.askstring("Nombre del nodo", "Nombre del nodo:")
        if name:
            AddNode(current_graph, Node(name, x, y))
            actualizar_vecinos()
            plot_graph(current_graph)
        return

    nodo = find_closest_node(x, y)
    if nodo is None:
        return

    if modo == "segmento":
        selected_nodes.append(nodo)
        if len(selected_nodes) == 2:
            name = simpledialog.askstring("Nombre del segmento", "Nombre del segmento:")
            if name:
                AddSegment(current_graph, name, selected_nodes[0].name, selected_nodes[1].name)
                actualizar_vecinos()
            selected_nodes.clear()
            plot_graph(current_graph)

    elif modo == "vecinos":
        plot_neighbors(current_graph, nodo)

    elif modo == "camino":
        selected_nodes.append(nodo)
        if len(selected_nodes) == 2:
            path = FindShortestPath(current_graph, selected_nodes[0].name, selected_nodes[1].name)
            if path:
                plot_path(current_graph, path)
            else:
                messagebox.showinfo("Sin camino", "No existe un camino entre los nodos seleccionados.")
            selected_nodes.clear()

    elif modo == "alcanzabilidad":
        plot_reachability(current_graph, nodo)

    elif event.button == 3:
        if messagebox.askyesno("Eliminar nodo", f"¿Eliminar nodo '{nodo.name}'?"):
            RemoveNode(current_graph, nodo.name)
            actualizar_vecinos()
            plot_graph(current_graph)

def actualizar_vecinos():
    for n in current_graph.nodes:
        n.neighbors = []
    for seg in current_graph.segments:
        o = next((n for n in current_graph.nodes if n.name == seg.origin.name), None)
        d = next((n for n in current_graph.nodes if n.name == seg.destination.name), None)
        if o and d:
            o.AddNeighbor(d)

def plot_path(g, path):
    global fig, ax, canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    fig, ax = plt.subplots()
    ax.set_title(f"Camino más corto (coste: {path.cost:.2f})")
    ax.grid(True, linestyle='--', color='lightgray')
    for seg in g.segments:
        x = [seg.origin.x, seg.destination.x]
        y = [seg.origin.y, seg.destination.y]
        ax.plot(x, y, 'gray', alpha=0.3)
    for i in range(len(path.nodes) - 1):
        x = [path.nodes[i].x, path.nodes[i+1].x]
        y = [path.nodes[i].y, path.nodes[i+1].y]
        ax.annotate('', xy=(x[1], y[1]), xytext=(x[0], y[0]),
                    arrowprops=dict(facecolor='red', edgecolor='red', shrink=0.05, width=1.5, headwidth=8))
    for n in g.nodes:
        color = 'blue' if n == path.nodes[0] else 'green' if n == path.nodes[-1] else 'gray'
        ax.plot(n.x, n.y, 'o', color=color)
        ax.text(n.x + 0.2, n.y + 0.2, n.name)
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()
    fig.canvas.mpl_connect("button_press_event", on_click)

def plot_neighbors(g, node):
    actualizar_vecinos()
    vecinos = set(n.name for n in node.neighbors)
    global fig, ax, canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    fig, ax = plt.subplots()
    ax.set_title(f"Vecinos de {node.name}")
    for seg in g.segments:
        x = [seg.origin.x, seg.destination.x]
        y = [seg.origin.y, seg.destination.y]
        color = 'red' if seg.origin.name == node.name else 'gray'
        ax.plot(x, y, color)
    for n in g.nodes:
        color = 'blue' if n.name == node.name else 'green' if n.name in vecinos else 'gray'
        ax.plot(n.x, n.y, 'o', color=color)
        ax.text(n.x + 0.2, n.y + 0.2, n.name)
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()
    fig.canvas.mpl_connect("button_press_event", on_click)

def plot_reachability(g, node):
    visited = set()
    queue = deque([node])
    actualizar_vecinos()
    while queue:
        actual = queue.popleft()
        if actual.name not in visited:
            visited.add(actual.name)
            queue.extend(nb for nb in actual.neighbors if nb.name not in visited)
    global fig, ax, canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    fig, ax = plt.subplots()
    ax.set_title(f"Alcanzables desde {node.name}")
    for seg in g.segments:
        x = [seg.origin.x, seg.destination.x]
        y = [seg.origin.y, seg.destination.y]
        if seg.origin.name in visited and seg.destination.name in visited:
            ax.plot(x, y, 'green')
        else:
            ax.plot(x, y, 'gray', alpha=0.2)
    for n in g.nodes:
        color = 'blue' if n.name == node.name else 'green' if n.name in visited else 'gray'
        ax.plot(n.x, n.y, 'o', color=color)
        ax.text(n.x + 0.2, n.y + 0.2, n.name)
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()
    fig.canvas.mpl_connect("button_press_event", on_click)

def cargar():
    global current_graph
    path = filedialog.askopenfilename()
    if path:
        if path.endswith("graph_data.txt"):
            current_graph = CreateGraph_2()
        elif path.endswith("graph_example.txt"):
            current_graph = CreateGraph_1()
        else:
            current_graph = LoadGraphFromFile(path)
        actualizar_vecinos()
        plot_graph(current_graph)

def nuevo():
    global current_graph
    current_graph = Graph()
    plot_graph(current_graph)

def guardar():
    if not current_graph:
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if path:
        SaveGraphToFile(current_graph, path)
        messagebox.showinfo("Guardado", "Grafo guardado correctamente.")

def mostrar_ejemplo(nombre_archivo):
    global current_graph
    if nombre_archivo == "graph_data.txt":
        current_graph = CreateGraph_2()
    elif nombre_archivo == "graph_example.txt":
        current_graph = CreateGraph_1()
    else:
        current_graph = LoadGraphFromFile(nombre_archivo)
    actualizar_vecinos()
    plot_graph(current_graph)

tk.Button(frame_buttons, text="📊 Mostrar Grafo de Ejemplo", command=lambda: mostrar_ejemplo("graph_example.txt"), width=30).pack(pady=3)
tk.Button(frame_buttons, text="📊 Mostrar Mi Grafo Guardado", command=lambda: mostrar_ejemplo("graph_data.txt"), width=30).pack(pady=3)
tk.Button(frame_buttons, text="📂 Cargar Grafo", command=cargar, width=30).pack(pady=3)
tk.Button(frame_buttons, text="🆕 Nuevo Grafo", command=nuevo, width=30).pack(pady=3)
tk.Button(frame_buttons, text="💾 Guardar Grafo", command=guardar, width=30).pack(pady=3)
tk.Label(frame_buttons, text="Modos de interacción:").pack(pady=(10,2))
tk.Button(frame_buttons, text="➕ Añadir Nodo", command=lambda: set_modo("nodo"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🔗 Añadir Segmento", command=lambda: set_modo("segmento"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="👁️ Ver Vecinos", command=lambda: set_modo("vecinos"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🌐 Alcanzabilidad", command=lambda: set_modo("alcanzabilidad"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="📏 Camino más corto", command=lambda: set_modo("camino"), width=30).pack(pady=2)

root.mainloop()
