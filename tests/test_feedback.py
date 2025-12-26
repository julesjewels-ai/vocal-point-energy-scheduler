import unittest
from datetime import datetime, timedelta
from src.feedback import FeedbackGenerator
from src.domain import EnergyLevel

class TestFeedbackGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = FeedbackGenerator()

    def test_no_entries(self):
        feedback = self.generator.generate_feedback([])
        self.assertIn("No energy logs found", feedback)

    def test_few_entries(self):
        entries = [
            {"timestamp": datetime.now().isoformat(), "energy_level": "high"}
        ]
        feedback = self.generator.generate_feedback(entries)
        self.assertIn("You have logged 1 entries", feedback)
        self.assertIn("Keep going", feedback)

    def test_peak_trend(self):
        # Create 3 high energy entries at 10 AM
        base_time = datetime(2023, 1, 1, 10, 0, 0)
        entries = [
            {"timestamp": base_time.isoformat(), "energy_level": "high"},
            {"timestamp": (base_time + timedelta(days=1)).isoformat(), "energy_level": "high"},
            {"timestamp": (base_time + timedelta(days=2)).isoformat(), "energy_level": "high"},
            # And a low one at 2 PM
            {"timestamp": datetime(2023, 1, 1, 14, 0, 0).isoformat(), "energy_level": "low"},
        ]

        feedback = self.generator.generate_feedback(entries)

        self.assertIn("Analysis based on 4 entries", feedback)
        self.assertIn("Peak Energy", feedback)
        self.assertIn("10 AM", feedback) # Should detect 10 AM as peak

    def test_low_trend(self):
         # Create 3 low energy entries at 2 PM (14:00)
        base_time = datetime(2023, 1, 1, 14, 0, 0)
        entries = [
            {"timestamp": base_time.isoformat(), "energy_level": "low"},
            {"timestamp": (base_time + timedelta(days=1)).isoformat(), "energy_level": "low"},
            {"timestamp": (base_time + timedelta(days=2)).isoformat(), "energy_level": "low"},
             # High one at 9 AM
            {"timestamp": datetime(2023, 1, 1, 9, 0, 0).isoformat(), "energy_level": "high"},
        ]

        feedback = self.generator.generate_feedback(entries)
        self.assertIn("Low Energy", feedback)
        self.assertIn("2 PM", feedback) # Should detect 2 PM as low

if __name__ == '__main__':
    unittest.main()
