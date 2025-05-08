class NavAirport:
    def __init__(self, name: str):
        self.name = name
        self.sids = []
        self.stars = []

    def add_sid(self, navpoint_number: int):
        if navpoint_number not in self.sids:
            self.sids.append(navpoint_number)

    def add_star(self, navpoint_number: int):
        if navpoint_number not in self.stars:
            self.stars.append(navpoint_number)

    def __repr__(self):
        return (f"NavAirport({self.name}, "
                f"SIDs={self.sids}, "
                f"STARs={self.stars})")
