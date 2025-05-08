from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport
import heapq

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []
        self.navpoints_by_number = {}
        self.navpoints_by_name = {}

    def clear(self):
        self.navpoints.clear()
        self.navsegments.clear()
        self.navairports.clear()
        self.navpoints_by_number.clear()
        self.navpoints_by_name.clear()

    def load_from_files(self, nav_path, seg_path, aer_path):
        self.clear()

        # NAVPOINTS
        with open(nav_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 4:
                    continue
                number = int(parts[0])
                name = parts[1]
                lat = float(parts[2])
                lon = float(parts[3])
                self.create_point(number, name, lat, lon)

        # SEGMENTS
        with open(seg_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 3:
                    continue
                origin = int(parts[0])
                dest = int(parts[1])
                dist = float(parts[2])
                self.navsegments.append(NavSegment(origin, dest, dist))

        # AIRPORTS, SIDs y STARs (resiliente a errores)
        with open(aer_path, 'r') as f:
            current = None
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if not line.endswith(".D") and not line.endswith(".A"):
                    # Definir nuevo aeropuerto, aunque no sea un nodo
                    current = NavAirport(line)
                    self.navairports.append(current)

                elif line.endswith(".D") and current:
                    base = line[:-2]
                    punto = self.navpoints_by_name.get(base)
                    if punto:
                        current.add_sid(punto.number)

                elif line.endswith(".A") and current:
                    base = line[:-2]
                    punto = self.navpoints_by_name.get(base)
                    if punto:
                        current.add_star(punto.number)

    def create_point(self, number, name, lat, lon):
        point = NavPoint(number, name, lat, lon)
        self.navpoints.append(point)
        self.navpoints_by_number[number] = point
        self.navpoints_by_name[name] = point
        return point

    def create_segment(self, origin, destination):
        distance = origin.distance_to(destination)
        self.navsegments.append(NavSegment(origin.number, destination.number, distance))

    def delete_point(self, number):
        if number not in self.navpoints_by_number:
            return
        point = self.navpoints_by_number[number]
        self.navpoints.remove(point)
        del self.navpoints_by_number[number]
        del self.navpoints_by_name[point.name]
        self.navsegments = [
            s for s in self.navsegments
            if s.origin_number != number and s.destination_number != number
        ]

    def get_neighbors(self, point):
        vecinos = []
        for seg in self.navsegments:
            if seg.origin_number == point.number:
                destino = self.navpoints_by_number.get(seg.destination_number)
                if destino:
                    vecinos.append(destino)
            elif seg.destination_number == point.number:
                origen = self.navpoints_by_number.get(seg.origin_number)
                if origen:
                    vecinos.append(origen)
        return vecinos

    def shortest_path(self, origen, destino):
        distancias = {p.number: float('inf') for p in self.navpoints}
        anteriores = {}
        visitados = set()
        distancias[origen.number] = 0
        heap = [(0, origen.number)]

        while heap:
            coste_actual, actual = heapq.heappop(heap)
            if actual in visitados:
                continue
            visitados.add(actual)

            if actual == destino.number:
                break

            for seg in self.navsegments:
                if seg.origin_number == actual:
                    vecino = seg.destination_number
                    nuevo_coste = coste_actual + seg.distance
                    if nuevo_coste < distancias[vecino]:
                        distancias[vecino] = nuevo_coste
                        anteriores[vecino] = actual
                        heapq.heappush(heap, (nuevo_coste, vecino))

        if distancias[destino.number] == float('inf'):
            return None, float('inf')

        # Reconstrucción del camino
        camino = []
        actual = destino.number
        while actual != origen.number:
            camino.append(self.navpoints_by_number[actual])
            actual = anteriores.get(actual)
            if actual is None:
                return None, float('inf')
        camino.append(origen)
        camino.reverse()
        return camino, distancias[destino.number]
