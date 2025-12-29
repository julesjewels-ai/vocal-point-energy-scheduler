from typing import Dict, Any
from datetime import datetime
from src.interfaces import IStorage, IEnergyAnalyzer, IFeedbackGenerator
from src.domain import EnergyLevel

class EnergyService:
    def __init__(self, storage: IStorage, analyzer: IEnergyAnalyzer, feedback_generator: IFeedbackGenerator):
        self.storage = storage
        self.analyzer = analyzer
        self.feedback_generator = feedback_generator

    def record_entry(self, text: str, metrics: Dict[str, Any]) -> EnergyLevel:
        energy_level = self.analyzer.analyze(text, metrics)

        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "text": text,
            "metrics": metrics,
            "energy_level": energy_level.value
        }
        self.storage.save_entry(new_entry)
        return energy_level

    def get_feedback(self) -> str:
        entries = self.storage.load_entries()
        return self.feedback_generator.generate_feedback(entries)

    def clear_history(self):
        self.storage.clear_entries()
