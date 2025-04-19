from prometheus_client import Counter, Histogram, Gauge
from typing import Optional
import time

class BoatMetrics:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.rowing_operations = Counter(
            'boat_rowing_operations_total',
            'Total number of rowing operations',
            ['boat_name']
        )
        
        self.rowing_duration = Histogram(
            'boat_rowing_duration_seconds',
            'Duration of rowing operations',
            ['boat_name'],
            buckets=[0.1, 0.5, 1.0, 2.0, 5.0]
        )
        
        self.current_speed = Gauge(
            'boat_current_speed',
            'Current speed of the boat',
            ['boat_name']
        )
        
        self.oar_usage = Counter(
            'boat_oar_usage_total',
            'Total number of oar usages',
            ['boat_name', 'oar_id']
        )
        
        self.errors = Counter(
            'boat_errors_total',
            'Total number of errors',
            ['boat_name', 'error_type']
        )
        
        self._initialized = True

    def record_rowing(self, boat_name: str, duration: float) -> None:
        self.rowing_operations.labels(boat_name=boat_name).inc()
        self.rowing_duration.labels(boat_name=boat_name).observe(duration)

    def update_speed(self, boat_name: str, speed: float) -> None:
        self.current_speed.labels(boat_name=boat_name).set(speed)

    def record_oar_usage(self, boat_name: str, oar_id: str) -> None:
        self.oar_usage.labels(boat_name=boat_name, oar_id=oar_id).inc()

    def record_error(self, boat_name: str, error_type: str) -> None:
        self.errors.labels(boat_name=boat_name, error_type=error_type).inc()

class MetricsTimer:
    def __init__(self, metrics: BoatMetrics, boat_name: str):
        self.metrics = metrics
        self.boat_name = boat_name
        self.start_time: Optional[float] = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is not None:
            duration = time.time() - self.start_time
            self.metrics.record_rowing(self.boat_name, duration)
            if exc_type is not None:
                self.metrics.record_error(
                    self.boat_name,
                    exc_type.__name__ if exc_type else 'unknown'
                ) 