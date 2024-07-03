from dataclasses import dataclass

@dataclass
class Genere:
    GenreId: int
    Name: str

    def __hash__(self):
        return hash(self.GenreId)