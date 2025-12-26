from typing import List
from src.analyzer import EnergyLevel
from src.calendar_api import Task

class Scheduler:
    def __init__(self):
        pass

    def schedule_tasks(self, tasks: List[Task], current_energy: EnergyLevel) -> List[Task]:
        """
        Reorder tasks based on current energy level.
        Tasks matching the current energy level are prioritized.
        """
        matching_tasks = []
        other_tasks = []

        # Logic:
        # If High energy: Prioritize High -> Medium -> Low
        # If Medium energy: Prioritize Medium -> Low -> High (High might be too much)
        # If Low energy: Prioritize Low -> Medium -> High

        priority_map = {
            EnergyLevel.HIGH: [EnergyLevel.HIGH, EnergyLevel.MEDIUM, EnergyLevel.LOW],
            EnergyLevel.MEDIUM: [EnergyLevel.MEDIUM, EnergyLevel.LOW, EnergyLevel.HIGH],
            EnergyLevel.LOW: [EnergyLevel.LOW, EnergyLevel.MEDIUM, EnergyLevel.HIGH]
        }

        preferred_order = priority_map[current_energy]

        sorted_tasks = sorted(tasks, key=lambda t: preferred_order.index(t.required_energy))

        return sorted_tasks

    def get_recommendation(self, tasks: List[Task], current_energy: EnergyLevel) -> str:
        if not tasks:
            return "No tasks available."

        top_task = self.schedule_tasks(tasks, current_energy)[0]

        if current_energy == EnergyLevel.HIGH:
            return f"You are in high energy! Great time to tackle: {top_task.title}"
        elif current_energy == EnergyLevel.MEDIUM:
            return f"Your energy is steady. Good time for: {top_task.title}"
        else: # Low
            return f"You seem low on energy. Take it easy with: {top_task.title}"
