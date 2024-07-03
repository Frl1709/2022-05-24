from dataclasses import dataclass

@dataclass
class Track:
    TrackId: int
    Name: str
    AlbumId: int
    MediaTypeId: int
    GenreId: int
    Milliseconds: int
    Bytes: int

    def __hash__(self):
        return hash(self.TrackId)
