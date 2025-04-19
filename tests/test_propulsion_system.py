import pytest
from core.propulsion_system import PropulsionSystem, PropulsionType

def test_propulsion_system_initialization():
    system = PropulsionSystem(type_=PropulsionType.MANUAL)
    assert system.type_ == PropulsionType.MANUAL
    assert system.power is None
    assert not system.is_active
    assert system.current_speed == 0.0

def test_propulsion_system_with_power():
    system = PropulsionSystem(type_=PropulsionType.MECHANICAL, power=100.0)
    assert system.type_ == PropulsionType.MECHANICAL
    assert system.power == 100.0

def test_propulsion_system_activate():
    system = PropulsionSystem(type_=PropulsionType.MANUAL)
    system.activate(5.0)
    assert system.is_active
    assert system.current_speed == 5.0

def test_propulsion_system_activate_negative_speed():
    system = PropulsionSystem(type_=PropulsionType.MANUAL)
    with pytest.raises(ValueError):
        system.activate(-5.0)

def test_propulsion_system_deactivate():
    system = PropulsionSystem(type_=PropulsionType.MANUAL)
    system.activate(5.0)
    system.deactivate()
    assert not system.is_active
    assert system.current_speed == 0.0

def test_propulsion_system_adjust_speed():
    system = PropulsionSystem(type_=PropulsionType.MANUAL)
    system.activate(5.0)
    system.adjust_speed(3.0)
    assert system.current_speed == 8.0

def test_propulsion_system_adjust_speed_negative():
    system = PropulsionSystem(type_=PropulsionType.MANUAL)
    system.activate(5.0)
    with pytest.raises(ValueError):
        system.adjust_speed(-10.0)

def test_propulsion_system_get_status():
    system = PropulsionSystem(type_=PropulsionType.MANUAL, power=100.0)
    system.activate(5.0)
    status = system.get_status()
    assert status["type"] == "manual"
    assert status["power"] == 100.0
    assert status["is_active"] is True
    assert status["current_speed"] == 5.0 