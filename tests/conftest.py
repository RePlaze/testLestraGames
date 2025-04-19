import pytest

from core.boat import Boat
from core.oar import Oar
from core.propulsion_system import PropulsionSystem, PropulsionType
from utils.metrics import BoatMetrics
from utils.logging_config import configure_logging, get_logger

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    configure_logging(level="DEBUG")

@pytest.fixture
def logger():
    return get_logger("test")

@pytest.fixture(scope="session")
def metrics():
    return BoatMetrics()

@pytest.fixture
def sample_oar():
    return Oar(length=2.5, material="wood")

@pytest.fixture
def sample_propulsion():
    return PropulsionSystem(type_=PropulsionType.MANUAL)

@pytest.fixture
def sample_boat(sample_oar, sample_propulsion, metrics):
    oars = [sample_oar, sample_oar]
    return Boat(
        name="TestBoat",
        weight=100,
        oars=oars,
        propulsion_system=sample_propulsion,
        metrics=metrics
    )

@pytest.fixture
def async_boat(sample_boat):
    async def async_wrapper():
        return sample_boat
    return async_wrapper

@pytest.fixture(autouse=True)
def mock_time(monkeypatch):
    import time
    start_time = time.time()
    
    def mock_time_func():
        return start_time
    
    monkeypatch.setattr(time, 'time', mock_time_func) 