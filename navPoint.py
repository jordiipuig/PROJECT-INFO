class NavPoint:
    def __init__(self, number: int, name: str, latitude: float, longitude: float):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, other: 'NavPoint') -> float:
        """Return the Euclidean distance to another NavPoint."""
        dx = self.latitude - other.latitude
        dy = self.longitude - other.longitude
        return (dx ** 2 + dy ** 2) ** 0.5

    def __eq__(self, other):
        return isinstance(other, NavPoint) and self.number == other.number

    def __hash__(self):
        return hash(self.number)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f"NavPoint({self.number}, {self.name})"
