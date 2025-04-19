from abc import ABC, abstractmethod
from typing import Protocol, Dict, Any

class Movable(Protocol):
    def move(self, force: float) -> None:
        ...

    def stop(self) -> None:
        ...

    def get_status(self) -> Dict[str, Any]:
        ...

class PropulsionSystem(Protocol):
    def activate(self, initial_speed: float = 0.0) -> None:
        ...

    def deactivate(self) -> None:
        ...

    def adjust_speed(self, speed_change: float) -> None:
        ...

    def get_status(self) -> Dict[str, Any]:
        ...

class BoatComponent(ABC):
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

class Observable(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)

    def notify(self, event: str, **kwargs) -> None:
        for observer in self._observers:
            observer.update(event, **kwargs) 