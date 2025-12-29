from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional

class EnergyLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class EnergyEntry:
    timestamp: str
    text: str
    metrics: Dict
    energy_level: str
