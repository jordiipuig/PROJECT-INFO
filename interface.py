import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import math

plt.style.use('seaborn-v0_8')
import os
import webbrowser

from airSpace import AirSpace
from graph import *
from path import PlotPath
from graph import FindShortestPath, LoadGraphFromFile, CreateGraph_1, SaveGraphToFile
from kml_exporter import export_navpoints_to_kml, export_segments_to_kml, export_path_to_kml

root = tk.Tk()
root.title("Visualizador del Espacio Aéreo y Grafos Clásicos")
root.geometry("1250x800")

# Estilo moderno con ttk
style = ttk.Style(root)
style.theme_use('clam')
style.configure('TButton', font=('Segoe UI', 10), padding=5)
style.configure('TLabel', font=('Segoe UI', 11))

frame_buttons = ttk.Frame(root)
frame_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

canvas_buttons = tk.Canvas(frame_buttons, borderwidth=0, width=340)
scrollbar_buttons = ttk.Scrollbar(frame_buttons, orient="vertical", command=canvas_buttons.yview)
scrollable_frame = ttk.Frame(canvas_buttons)

scrollable_frame.bind(
    "<Configure>", lambda e: canvas_buttons.configure(scrollregion=canvas_buttons.bbox("all"))
)

canvas_buttons.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas_buttons.configure(yscrollcommand=scrollbar_buttons.set)

canvas_buttons.pack(side="left", fill="both", expand=True)
scrollbar_buttons.pack(side="right", fill="y")

frame_plot = ttk.Frame(root)
frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

airspace = AirSpace()
canvas = None
fig = None
ax = None
modo = "navegar"
selected_nodes = []
mostrar_costes = True
mostrar_nombres = True
current_graph = None
camino_actual = []

# === FUNCIONES NUEVAS ===


def abrir_google_earth():
    try:
        # Intentar abrir Google Earth Pro desde su ruta típica en Windows
        ruta_windows = r"C:\Program Files\Google\Google Earth Pro\client\googleearth.exe"
        if os.path.exists(ruta_windows):
            os.startfile(ruta_windows)
        else:
            # Como alternativa, abrir Google Earth Web
            webbrowser.open("https://earth.google.com/web/")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir Google Earth: {e}")

# === FUNCIONES PARA EXPORTAR A GOOGLE EARTH ===
def exportar_navpoints():
    path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
    if path:
        export_navpoints_to_kml(path, airspace.navpoints)
        messagebox.showinfo("Exportado", f"Puntos exportados a {path}")

def exportar_segmentos():
    path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
    if path:
        export_segments_to_kml(path, airspace.navsegments, airspace.navpoints_by_number)
        messagebox.showinfo("Exportado", f"Segmentos exportados a {path}")

def exportar_camino():
    global camino_actual
    if not camino_actual:
        messagebox.showwarning("Camino vacío", "No hay un camino más corto calculado actualmente.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".kml", filetypes=[("KML files", "*.kml")])
    if path:
        export_path_to_kml(path, camino_actual)
        messagebox.showinfo("Exportado", f"Camino más corto exportado a {path}")
# === FUNCIONES PARA GRAFO CLÁSICO ===
def actualizar_vecinos():
    for n in current_graph.nodes:
        n.neighbors = []
    for seg in current_graph.segments:
        o = next((n for n in current_graph.nodes if n.name == seg.origin.name), None)
        d = next((n for n in current_graph.nodes if n.name == seg.destination.name), None)
        if o and d:
            o.AddNeighbor(d)

def plot_graph(g):
    global fig, ax, canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    fig, ax = plt.subplots()
    ax.set_title("Grafo clásico")
    ax.grid(True, linestyle='--', color='lightgray')
    for seg in g.segments:
        x = [seg.origin.x, seg.destination.x]
        y = [seg.origin.y, seg.destination.y]
        ax.plot(x, y, 'gray', alpha=0.5)
    for n in g.nodes:
        ax.plot(n.x, n.y, 'o', color='blue')
        ax.annotate(n.name, (n.x, n.y), textcoords="offset points", xytext=(5, 5), ha='left')
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()

def cargar():
    global current_graph
    path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if path:
        current_graph = LoadGraphFromFile(path)
        actualizar_vecinos()
        plot_graph(current_graph)

def nuevo():
    global current_graph
    current_graph = CreateGraph_1()
    actualizar_vecinos()
    plot_graph(current_graph)

def mostrar_ejemplo(nombre_archivo):
    global current_graph
    current_graph = LoadGraphFromFile(nombre_archivo)
    actualizar_vecinos()
    plot_graph(current_graph)

def guardar():
    global current_graph
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if path:
        SaveGraphToFile(current_graph, path)
        messagebox.showinfo("Guardado", f"Grafo guardado en: {path}")

# === FUNCIONES AIRSPACE ===
def plot_airspace(highlight_nodes=None, highlight_edges=None, title="Espacio aéreo"):
    global canvas, fig, ax
    if canvas:
        canvas.get_tk_widget().destroy()
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.grid(True, linestyle='--', color='lightgray')
    ax.set_aspect('equal', adjustable='datalim')

    highlight_nodes = highlight_nodes or []
    highlight_edges = highlight_edges or []

    for seg in airspace.navsegments:
        p1 = airspace.navpoints_by_number[seg.origin_number]
        p2 = airspace.navpoints_by_number[seg.destination_number]
        x = [p1.longitude, p2.longitude]
        y = [p1.latitude, p2.latitude]
        if (p1, p2) in highlight_edges:
            ax.annotate('', xy=(x[1], y[1]), xytext=(x[0], y[0]),
                        arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->', lw=1.5))
        else:
            ax.plot(x, y, 'gray')
        if mostrar_costes:
            mx = (x[0] + x[1]) / 2
            my = (y[0] + y[1]) / 2
            ax.annotate(f"{seg.distance:.1f}", (mx, my), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

    for p in airspace.navpoints:
        color = 'red' if p in highlight_nodes else 'steelblue'
        ax.plot(p.longitude, p.latitude, 'o', color=color)
        if mostrar_nombres:
            ax.annotate(p.name, (p.longitude, p.latitude), textcoords="offset points", xytext=(5, 5), ha='left', fontsize=8)

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    fig.canvas.mpl_connect("button_press_event", on_click)
    fig.canvas.mpl_connect("scroll_event", on_scroll)

def set_modo(nuevo_modo):
    global modo, selected_nodes
    modo = nuevo_modo
    selected_nodes.clear()
    messagebox.showinfo("Modo activado", f"Modo '{modo}' activado.\nHaz clic sobre el grafo.")

def find_closest_point(x, y):
    if not airspace.navpoints:
        return None
    return min(airspace.navpoints, key=lambda p: ((p.longitude - x)**2 + (p.latitude - y)**2)**0.5)

def on_click(event):
    global modo, selected_nodes, camino_actual
    if not event.inaxes:
        return
    x, y = event.xdata, event.ydata

    if modo == "nodo":
        name = simpledialog.askstring("Nombre del nodo", "Nombre del nodo:")
        if name:
            number = max(p.number for p in airspace.navpoints) + 1
            airspace.create_point(number, name, y, x)
            plot_airspace()
        return

    point = find_closest_point(x, y)
    if point is None:
        return

    if modo == "segmento":
        selected_nodes.append(point)
        if len(selected_nodes) == 2:
            airspace.create_segment(selected_nodes[0], selected_nodes[1])
            selected_nodes.clear()
            plot_airspace()

    elif modo == "vecinos":
        mostrar_vecinos_manual(point)

    elif modo == "camino":
        selected_nodes.append(point)
        if len(selected_nodes) == 2:
            camino, coste = airspace.shortest_path(selected_nodes[0], selected_nodes[1])
            if not camino:
                messagebox.showinfo("Sin camino", "No hay camino posible entre esos puntos.")
                camino_actual = []
            else:
                camino_actual = camino
                edges = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
                messagebox.showinfo("Camino", f"{camino[0].name} → {camino[-1].name}\nCoste total: {coste:.2f} km")
                plot_airspace(highlight_nodes=camino, highlight_edges=edges, title="Camino más corto")
            selected_nodes.clear()

    elif modo == "alcanzabilidad":
        mostrar_alcanzables_manual(point)

    elif modo == "sidsstars":
        mostrar_sids_stars()

    elif event.button == 3:
        if messagebox.askyesno("Eliminar nodo", f"¿Eliminar nodo '{point.name}'?"):
            airspace.delete_point(point.number)
            plot_airspace()


def on_scroll(event):
    base_scale = 1.1
    ax = event.canvas.figure.axes[0]
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    xdata = event.xdata
    ydata = event.ydata
    if xdata is None or ydata is None:
        return

    if event.button == 'up':
        scale_factor = 1 / base_scale
    elif event.button == 'down':
        scale_factor = base_scale
    else:
        scale_factor = 1

    new_width = max((xlim[1] - xlim[0]) * scale_factor, 0.01)
    new_height = max((ylim[1] - ylim[0]) * scale_factor, 0.01)
    relx = (xdata - xlim[0]) / (xlim[1] - xlim[0])
    rely = (ydata - ylim[0]) / (ylim[1] - ylim[0])
    new_xlim = [xdata - new_width * relx, xdata + new_width * (1 - relx)]
    new_ylim = [ydata - new_height * rely, ydata + new_height * (1 - rely)]
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    event.canvas.draw()

def mostrar_vecinos_manual(point):
    segmentos_salientes = [s for s in airspace.navsegments if s.origin_number == point.number]
    vecinos = [airspace.navpoints_by_number[s.destination_number] for s in segmentos_salientes]
    edges = [(point, v) for v in vecinos]
    plot_airspace(highlight_nodes=[point] + vecinos, highlight_edges=edges, title=f"Vecinos de {point.name}")

def mostrar_alcanzables_manual(point):
    visitados = set()
    cola = [point]
    edges = []
    while cola:
        actual = cola.pop(0)
        if actual.number in visitados:
            continue
        visitados.add(actual.number)
        for seg in airspace.navsegments:
            if seg.origin_number == actual.number:
                destino = airspace.navpoints_by_number[seg.destination_number]
                if destino.number not in visitados:
                    cola.append(destino)
                    edges.append((actual, destino))
    nodos = [airspace.navpoints_by_number[n] for n in visitados]
    plot_airspace(highlight_nodes=nodos, highlight_edges=edges, title=f"Alcanzables desde {point.name}")

def mostrar_sids_stars():
    nodos = []
    for aeropuerto in airspace.navairports:
        for sid in aeropuerto.sids:
            if sid in airspace.navpoints_by_number:
                nodos.append(airspace.navpoints_by_number[sid])
        for star in aeropuerto.stars:
            if star in airspace.navpoints_by_number:
                nodos.append(airspace.navpoints_by_number[star])
    plot_airspace(highlight_nodes=nodos, title="SIDs y STARs destacados")

def toggle_costes():
    global mostrar_costes
    mostrar_costes = not mostrar_costes
    plot_airspace()

def toggle_nombres():
    global mostrar_nombres
    mostrar_nombres = not mostrar_nombres
    plot_airspace()

# === BOTONES DE LA INTERFAZ ===
ttk.Label(scrollable_frame, text="Espacio aéreo moderno:").pack(pady=(10, 2))
ttk.Button(scrollable_frame, text="\U0001F1E8 Catalunya", command=lambda: airspace.load_from_files("data/Cat_nav.txt", "data/Cat_seg.txt", "data/Cat_aer.txt") or plot_airspace(title="Espacio aéreo de Catalunya"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="\U0001F1EA España", command=lambda: airspace.load_from_files("data/Spain_nav.txt", "data/Spain_seg.txt", "data/Spain_aer.txt") or plot_airspace(title="Espacio aéreo de España"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="\U0001F1EA\U0001F1FA Europa", command=lambda: airspace.load_from_files("data/ECAC_nav.txt", "data/ECAC_seg.txt", "data/ECAC_aer.txt") or plot_airspace(title="Espacio aéreo de Europa"), width=30).pack(pady=2)

ttk.Label(scrollable_frame, text="Modos de interacción:").pack(pady=(10, 2))
ttk.Button(scrollable_frame, text="➕ Añadir Nodo", command=lambda: set_modo("nodo"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="🔗 Añadir Segmento", command=lambda: set_modo("segmento"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="👁️ Ver Vecinos", command=lambda: set_modo("vecinos"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="🌐 Alcanzabilidad", command=lambda: set_modo("alcanzabilidad"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="📏 Camino más corto", command=lambda: set_modo("camino"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="🛫 Mostrar SIDs y STARs", command=lambda: set_modo("sidsstars"), width=30).pack(pady=2)

ttk.Button(scrollable_frame, text="🌍 Abrir Google Earth", command=abrir_google_earth, width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="🧱 Mostrar/Ocultar Nombres", command=toggle_nombres, width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="📀 Mostrar/Ocultar Distancias", command=toggle_costes, width=30).pack(pady=2)

ttk.Label(scrollable_frame, text="Grafo clásico:").pack(pady=(10, 2))
ttk.Button(scrollable_frame, text="📂 Cargar Grafo", command=cargar, width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="🆕 Nuevo Grafo", command=nuevo, width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="📊 Mostrar Mi Grafo Guardado", command=lambda: mostrar_ejemplo("graph_data.txt"), width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="📀 Guardar Grafo", command=guardar, width=30).pack(pady=2)
ttk.Label(scrollable_frame, text="Exportar a Google Earth:").pack(pady=(10, 2))
ttk.Button(scrollable_frame, text="📤 Exportar Puntos (KML)", command=exportar_navpoints, width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="📤 Exportar Rutas (KML)", command=exportar_segmentos, width=30).pack(pady=2)
ttk.Button(scrollable_frame, text="📤 Exportar Camino (KML)", command=exportar_camino, width=30).pack(pady=2)
root.mainloop()