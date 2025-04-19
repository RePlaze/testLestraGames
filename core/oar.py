from interfaces.interfaces import BoatComponent

class Oar(BoatComponent):
    def __init__(self, length: float, material: str):
        self.length = length
        self.material = material
        self.position = 0
        self.is_moving = False

    def move(self, force: float) -> None:
        if force < 0:
            raise ValueError("Сила не может быть отрицательной")
        
        self.is_moving = True
        self.position += force / self.length
    
    def stop(self) -> None:
        self.is_moving = False
        self.position = 0

    def get_status(self) -> dict:
        return {
            "length": self.length,
            "material": self.material,
            "position": self.position,
            "is_moving": self.is_moving
        }

    def reset(self) -> None:
        self.stop() 