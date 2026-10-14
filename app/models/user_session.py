"""RF-01/RNF-04: contrato de sesión efímera con dos fotos en memoria."""
from dataclasses import dataclass
@dataclass
class UserSession:
    token: str
    face_photo: bytes | None = None
    body_photo: bytes | None = None
    def clear(self):
        """Descarta referencias; el almacén de sesiones y expiración se implementarán después."""
        self.face_photo = self.body_photo = None
