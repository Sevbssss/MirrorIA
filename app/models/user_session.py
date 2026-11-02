"""RF-01/RNF-04: sesión efímera del usuario; las fotografías viven solo en memoria."""
from dataclasses import dataclass, field
from time import time


@dataclass
class UserSession:
    token: str
    face_photo: bytes | None = None
    body_photo: bytes | None = None
    photos_confirmed: bool = False
    search_query: str | None = None
    search_filters: dict | None = None
    last_seen: float = field(default_factory=time)

    @property
    def has_photos(self) -> bool:
        return self.face_photo is not None and self.body_photo is not None

    def reset_progress(self) -> None:
        """Descarta lo que depende de las fotografías cuando estas cambian."""
        self.photos_confirmed = False
        self.search_query = None
        self.search_filters = None

    def clear(self) -> None:
        """Descarta las fotografías y todo lo derivado de ellas."""
        self.face_photo = self.body_photo = None
        self.reset_progress()
