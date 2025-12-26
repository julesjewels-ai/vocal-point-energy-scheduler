from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
from src.analyzer import EnergyLevel

@dataclass
class Task:
    id: str
    title: str
    required_energy: EnergyLevel
    duration_minutes: int
    deadline: Optional[datetime] = None

class Calendar:
    def __init__(self):
        self.tasks: List[Task] = []
        # Seed with some dummy data
        self._seed_data()

    def _seed_data(self):
        self.tasks = [
            Task("1", "Deep Work: Coding", EnergyLevel.HIGH, 60),
            Task("2", "Brainstorming Session", EnergyLevel.HIGH, 45),
            Task("3", "Reply to Emails", EnergyLevel.MEDIUM, 30),
            Task("4", "Team Sync", EnergyLevel.MEDIUM, 30),
            Task("5", "Organize Files", EnergyLevel.LOW, 20),
            Task("6", "Read Documentation", EnergyLevel.LOW, 30),
        ]

    def get_tasks(self) -> List[Task]:
        return self.tasks

    def add_task(self, task: Task):
        self.tasks.append(task)
