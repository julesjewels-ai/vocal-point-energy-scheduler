from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.domain import EnergyLevel, EnergyEntry

class IEnergyAnalyzer(ABC):
    @abstractmethod
    def analyze(self, text: str, metrics: Dict[str, Any] = None) -> EnergyLevel:
        pass

class IStorage(ABC):
    @abstractmethod
    def load_entries(self) -> List[Dict]:
        pass

    @abstractmethod
    def save_entry(self, entry: Dict):
        pass

    @abstractmethod
    def clear_entries(self):
        pass

class IFeedbackGenerator(ABC):
    @abstractmethod
    def generate_feedback(self, entries: List[Dict]) -> str:
        pass
