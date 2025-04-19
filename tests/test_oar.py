import pytest
from core.oar import Oar

def test_oar_initialization():
    oar = Oar(length=2.5, material="wood")
    assert oar.length == 2.5
    assert oar.material == "wood"
    assert oar.position == 0
    assert not oar.is_moving

def test_oar_move():
    oar = Oar(length=2.5, material="wood")
    oar.move(10)
    assert oar.position == 4.0  # 10 / 2.5
    assert oar.is_moving

def test_oar_move_negative_force():
    oar = Oar(length=2.5, material="wood")
    with pytest.raises(ValueError):
        oar.move(-10)

def test_oar_stop():
    oar = Oar(length=2.5, material="wood")
    oar.move(10)
    oar.stop()
    assert oar.position == 0
    assert not oar.is_moving

def test_oar_get_status():
    oar = Oar(length=2.5, material="wood")
    status = oar.get_status()
    assert status["length"] == 2.5
    assert status["material"] == "wood"
    assert status["position"] == 0
    assert not status["is_moving"] 