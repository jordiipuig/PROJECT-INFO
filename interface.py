import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from airSpace import AirSpace

root = tk.Tk()
root.title("Visualizador del Espacio Aéreo")
root.geometry("1100x800")

frame_buttons = tk.Frame(root)
frame_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

frame_plot = tk.Frame(root)
frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

airspace = AirSpace()
canvas = None
fig = None
ax = None
modo = "navegar"
selected_nodes = []
mostrar_costes = True
mostrar_nombres = True



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
        color = 'green' if (p1, p2) in highlight_edges else 'gray'
        if (p1, p2) in highlight_edges:
            ax.annotate('', xy=(x[1], y[1]), xytext=(x[0], y[0]),
                        arrowprops=dict(facecolor='red', edgecolor='red', arrowstyle='->', lw=1.5))
        else:
            ax.plot(x, y, color)
        if mostrar_costes:
            mx = (x[0] + x[1]) / 2
            my = (y[0] + y[1]) / 2
            ax.text(mx, my, f"{seg.distance:.1f}", fontsize=8)

    for p in airspace.navpoints:
        color = 'red' if p in highlight_nodes else 'steelblue'
        ax.plot(p.longitude, p.latitude, 'o', color=color)
        if mostrar_nombres:
            ax.text(p.longitude + 0.2, p.latitude + 0.2, p.name, fontsize=8)

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
    global modo, selected_nodes
    if not event.inaxes or not airspace.navpoints:
        return
    x, y = event.xdata, event.ydata

    if modo == "nodo":
        name = simpledialog.askstring("Nombre del nodo", "Nombre del nodo:")
        if name:
            number = max(p.number for p in airspace.navpoints) + 1
            new_point = airspace.create_point(number, name, y, x)
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
            else:
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



def toggle_costes():
    global mostrar_costes
    mostrar_costes = not mostrar_costes
    plot_airspace()

def toggle_nombres():
    global mostrar_nombres
    mostrar_nombres = not mostrar_nombres
    plot_airspace()

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

# === BOTONES COMPLETOS ===
tk.Label(frame_buttons, text="Cargar espacio aéreo:").pack(pady=(10, 2))
tk.Button(frame_buttons, text="🇨🇦 Catalunya", command=lambda: airspace.load_from_files("data/Cat_nav.txt", "data/Cat_seg.txt", "data/Cat_aer.txt") or plot_airspace(title="Espacio aéreo de Catalunya"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🇪🇸 España", command=lambda: airspace.load_from_files("data/Spain_nav.txt", "data/Spain_seg.txt", "data/Spain_aer.txt") or plot_airspace(title="Espacio aéreo de España"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🇪🇺 Europa", command=lambda: airspace.load_from_files("data/ECAC_nav.txt", "data/ECAC_seg.txt", "data/ECAC_aer.txt") or plot_airspace(title="Espacio aéreo de Europa"), width=30).pack(pady=2)

tk.Label(frame_buttons, text="Modos de interacción:").pack(pady=(10, 2))
tk.Button(frame_buttons, text="➕ Añadir Nodo", command=lambda: set_modo("nodo"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🔗 Añadir Segmento", command=lambda: set_modo("segmento"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="👁️ Ver Vecinos", command=lambda: set_modo("vecinos"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🌐 Alcanzabilidad", command=lambda: set_modo("alcanzabilidad"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="📏 Camino más corto", command=lambda: set_modo("camino"), width=30).pack(pady=2)
tk.Button(frame_buttons, text="🧭 Mostrar/Ocultar Nombres", command=toggle_nombres, width=30).pack(pady=2)
tk.Button(frame_buttons, text="🛫 Mostrar SIDs y STARs", command=lambda: set_modo("sidsstars"), width=30).pack(pady=2)


root.mainloop()
