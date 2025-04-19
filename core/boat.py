from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from interfaces.interfaces import Movable, BoatComponent, Observable
from .oar import Oar
from .propulsion_system import PropulsionSystem
from utils.metrics import BoatMetrics
from utils.logging_config import get_logger

logger = get_logger(__name__)

@dataclass
class Boat(Movable, BoatComponent, Observable):
    name: str
    weight: float
    oars: List[Oar]
    propulsion_system: PropulsionSystem
    metrics: BoatMetrics = field(default_factory=BoatMetrics)
    _speed: float = field(default=0.0, init=False)
    _is_moving: bool = field(default=False, init=False)
    _observers: List[Observable] = field(default_factory=list)

    def __post_init__(self):
        super().__init__()
        self._validate_components()

    def _validate_components(self) -> None:
        if not self.oars:
            raise ValueError("Лодка должна иметь хотя бы одно весло")
        if not self.propulsion_system:
            raise ValueError("Лодка должна иметь систему движения")

    def move(self, force: float) -> None:
        try:
            if force < 0:
                raise ValueError("Сила не может быть отрицательной")
                
            if not self._is_moving:
                self.propulsion_system.activate()
                self._is_moving = True
                self.notify("start_moving", force=force)

            self._speed = self._calculate_speed(force)
            self.propulsion_system.adjust_speed(self._speed)
            
            self.metrics.record_rowing(self.name, self._speed)
            self.notify("speed_changed", speed=self._speed)
            
            logger.info("boat_moving", 
                       boat_name=self.name,
                       speed=self._speed,
                       force=force)
        except Exception as e:
            self.metrics.record_error(self.name, str(e))
            logger.error("boat_move_error",
                        boat_name=self.name,
                        error=str(e))
            raise

    def stop(self) -> None:
        if self._is_moving:
            self._speed = 0.0
            self.propulsion_system.deactivate()
            self._is_moving = False
            self.notify("stopped")
            logger.info("boat_stopped", boat_name=self.name)

    def _calculate_speed(self, force: float) -> float:
        total_oar_length = sum(oar.length for oar in self.oars)
        return (force * total_oar_length) / self.weight

    def get_status(self) -> Dict[str, Any]:
        status = {
            "name": self.name,
            "weight": self.weight,
            "current_speed": self._speed,
            "is_moving": self._is_moving,
            "oars": [oar.get_status() for oar in self.oars],
            "propulsion": self.propulsion_system.get_status(),
            "propulsion_type": self.propulsion_system.type_.value,
            "oars_count": len(self.oars)
        }
        return status

    def reset(self) -> None:
        self._speed = 0.0
        self._is_moving = False
        self.propulsion_system.deactivate()
        for oar in self.oars:
            oar.reset()
        self.notify("reset")
        logger.info("boat_reset", boat_name=self.name) 