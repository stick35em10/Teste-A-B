# monitoring/metrics.py
import time
from prometheus_client import Counter, Histogram, Gauge

# Métricas Prometheus
conversion_events = Counter('ab_test_conversions_total', 
                           'Total conversion events', 
                           ['experiment', 'variant'])

assignment_events = Counter('ab_test_assignments_total',
                           'Total user assignments',
                           ['experiment', 'variant'])

experiment_duration = Histogram('ab_test_duration_seconds',
                               'Experiment duration in seconds')

active_experiments = Gauge('ab_test_active_experiments',
                          'Number of active experiments')

class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
    
    def record_conversion(self, experiment: str, variant: str, value: float = 1.0):
        conversion_events.labels(experiment=experiment, variant=variant).inc(value)
    
    def record_assignment(self, experiment: str, variant: str):
        assignment_events.labels(experiment=experiment, variant=variant).inc()