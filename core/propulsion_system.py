from enum import Enum
from typing import Optional
from interfaces.interfaces import PropulsionSystem as PropulsionSystemInterface

class PropulsionType(Enum):
    MANUAL = "manual"
    MECHANICAL = "mechanical"
    ELECTRIC = "electric"

class PropulsionSystem(PropulsionSystemInterface):
    def __init__(self, type_: PropulsionType, power: Optional[float] = None):
        if not isinstance(type_, PropulsionType):
            raise ValueError("type_ должен быть экземпляром PropulsionType")
        self.type_ = type_
        self.power = power
        self.is_active = False
        self.current_speed = 0.0

    def activate(self, initial_speed: float = 0.0) -> None:
        if initial_speed < 0:
            raise ValueError("Скорость не может быть отрицательной")
        
        self.is_active = True
        self.current_speed = initial_speed
    
    def deactivate(self) -> None:
        self.is_active = False
        self.current_speed = 0.0

    def adjust_speed(self, speed_change: float) -> None:
        new_speed = self.current_speed + speed_change
        if new_speed < 0:
            raise ValueError("Скорость не может быть отрицательной")
        
        self.current_speed = new_speed

    def get_status(self) -> dict:
        return {
            "type": self.type_.value,
            "power": self.power,
            "is_active": self.is_active,
            "current_speed": self.current_speed
        } 