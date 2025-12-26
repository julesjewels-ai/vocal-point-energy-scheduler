import unittest
from src.scheduler import Scheduler
from src.calendar_api import Task
from src.analyzer import EnergyLevel

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()
        self.tasks = [
            Task("1", "High Task", EnergyLevel.HIGH, 60),
            Task("2", "Med Task", EnergyLevel.MEDIUM, 30),
            Task("3", "Low Task", EnergyLevel.LOW, 20),
        ]

    def test_schedule_high_energy(self):
        sorted_tasks = self.scheduler.schedule_tasks(self.tasks, EnergyLevel.HIGH)
        # Expected order: HIGH, MEDIUM, LOW
        self.assertEqual(sorted_tasks[0].required_energy, EnergyLevel.HIGH)
        self.assertEqual(sorted_tasks[1].required_energy, EnergyLevel.MEDIUM)
        self.assertEqual(sorted_tasks[2].required_energy, EnergyLevel.LOW)

    def test_schedule_medium_energy(self):
        sorted_tasks = self.scheduler.schedule_tasks(self.tasks, EnergyLevel.MEDIUM)
        # Expected order: MEDIUM, LOW, HIGH
        self.assertEqual(sorted_tasks[0].required_energy, EnergyLevel.MEDIUM)
        self.assertEqual(sorted_tasks[1].required_energy, EnergyLevel.LOW)
        self.assertEqual(sorted_tasks[2].required_energy, EnergyLevel.HIGH)

    def test_schedule_low_energy(self):
        sorted_tasks = self.scheduler.schedule_tasks(self.tasks, EnergyLevel.LOW)
        # Expected order: LOW, MEDIUM, HIGH
        self.assertEqual(sorted_tasks[0].required_energy, EnergyLevel.LOW)
        self.assertEqual(sorted_tasks[1].required_energy, EnergyLevel.MEDIUM)
        self.assertEqual(sorted_tasks[2].required_energy, EnergyLevel.HIGH)

    def test_get_recommendation(self):
        rec = self.scheduler.get_recommendation(self.tasks, EnergyLevel.HIGH)
        self.assertIn("High Task", rec)
        self.assertIn("high energy", rec)

if __name__ == '__main__':
    unittest.main()
