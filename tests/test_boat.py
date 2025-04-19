import pytest
from core.boat import Boat
from core.oar import Oar
from core.propulsion_system import PropulsionSystem, PropulsionType

@pytest.fixture
def propulsion_system():
    return PropulsionSystem(type_=PropulsionType.MANUAL)

@pytest.fixture
def oars():
    return [Oar(2.5, "wood") for _ in range(2)]

@pytest.fixture
def boat(oars, propulsion_system):
    return Boat("Test Boat", 100.0, oars, propulsion_system)

def test_boat_initialization(boat, oars, propulsion_system):
    assert boat.name == "Test Boat"
    assert boat.weight == 100.0
    assert len(boat.oars) == 2
    assert boat.propulsion_system == propulsion_system
    assert boat._speed == 0.0
    assert not boat._is_moving
    assert len(boat._observers) == 0

def test_boat_move(boat):
    boat.move(10.0)
    assert boat._is_moving
    assert boat._speed > 0.0
    assert boat.propulsion_system.is_active

def test_boat_move_negative_force(boat):
    with pytest.raises(ValueError):
        boat.move(-5.0)
    assert not boat._is_moving
    assert boat._speed == 0.0

def test_boat_stop(boat):
    boat.move(10.0)
    boat.stop()
    assert not boat._is_moving
    assert boat._speed == 0.0
    assert not boat.propulsion_system.is_active

def test_boat_get_status(boat):
    status = boat.get_status()
    assert status["name"] == "Test Boat"
    assert status["weight"] == 100.0
    assert status["current_speed"] == 0.0
    assert not status["is_moving"]
    assert len(status["oars"]) == 2
    assert status["propulsion_type"] == "manual"
    assert status["oars_count"] == 2

def test_boat_reset(boat):
    boat.move(10.0)
    boat.reset()
    assert not boat._is_moving
    assert boat._speed == 0.0
    assert not boat.propulsion_system.is_active
    for oar in boat.oars:
        assert not oar.is_moving
        assert oar.position == 0

def test_boat_observer_notification(boat):
    class TestObserver:
        def __init__(self):
            self.events = []
        
        def update(self, event, **kwargs):
            self.events.append((event, kwargs))
    
    observer = TestObserver()
    boat.attach(observer)
    
    boat.move(10.0)
    assert ("start_moving", {"force": 10.0}) in observer.events
    assert ("speed_changed", {"speed": boat._speed}) in observer.events
    
    boat.stop()
    assert ("stopped", {}) in observer.events
    
    boat.reset()
    assert ("reset", {}) in observer.events 