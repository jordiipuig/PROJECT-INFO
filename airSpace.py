from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []
        self.navpoints_by_number = {}
        self.navpoints_by_name = {}

    def load_from_files(self, nav_path, seg_path, aer_path):
        # Cargar puntos de navegación
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

        # Cargar segmentos
        with open(seg_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) != 3:
                    continue
                origin = int(parts[0])
                dest = int(parts[1])
                dist = float(parts[2])
                self.navsegments.append(NavSegment(origin, dest, dist))

        # Cargar aeropuertos
        with open(aer_path, 'r') as f:
            current = None
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line in self.navpoints_by_name:
                    current = NavAirport(line)
                    self.navairports.append(current)
                elif line.endswith(".D") and current:
                    base = line[:-2]
                    if base in self.navpoints_by_name:
                        current.add_sid(self.navpoints_by_name[base].number)
                elif line.endswith(".A") and current:
                    base = line[:-2]
                    if base in self.navpoints_by_name:
                        current.add_star(self.navpoints_by_name[base].number)

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
        self.navsegments = [s for s in self.navsegments if s.origin_number != number and s.destination_number != number]

    def get_neighbors(self, point):
        neighbors = []
        segment_map = {}
        for s in self.navsegments:
            if s.origin_number not in segment_map:
                segment_map[s.origin_number] = []
            segment_map[s.origin_number].append(s.destination_number)

        for dest_number in segment_map.get(point.number, []):
            if dest_number in self.navpoints_by_number:
                neighbors.append(self.navpoints_by_number[dest_number])
        return neighbors

    def get_reachables(self, start_point):
        visited = set()
        queue = [start_point.number]
        while queue:
            current_number = queue.pop(0)
            if current_number in visited:
                continue
            visited.add(current_number)
            for seg in self.navsegments:
                if seg.origin_number == current_number and seg.destination_number not in visited:
                    queue.append(seg.destination_number)
        return [self.navpoints_by_number[n] for n in visited if n in self.navpoints_by_number]