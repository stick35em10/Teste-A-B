# core/experiment_manager.py
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from enum import Enum

class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"

class ExperimentManager:
    def __init__(self, db_session):
        self.db = db_session
    
    def create_experiment(self, name: str, variants: List[Dict], metrics: List[str]):
        """Cria um novo experimento"""
        experiment = {
            "name": name,
            "variants": variants,
            "metrics": metrics,
            "status": ExperimentStatus.DRAFT,
            "created_at": datetime.utcnow(),
            "traffic_percentage": 100  # 100% do tráfego
        }
        return self.db.experiments.insert_one(experiment)
    
    def start_experiment(self, experiment_id: str):
        """Inicia um experimento"""
        return self.db.experiments.update_one(
            {"_id": experiment_id},
            {"$set": {"status": ExperimentStatus.RUNNING, "started_at": datetime.utcnow()}}
        )