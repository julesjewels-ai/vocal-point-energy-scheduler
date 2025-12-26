import unittest
from src.analyzer import EnergyAnalyzer, EnergyLevel

class TestEnergyAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = EnergyAnalyzer()

    def test_high_energy_text(self):
        text = "I am feeling excited and ready to go!"
        level = self.analyzer.analyze(text)
        self.assertEqual(level, EnergyLevel.HIGH)

    def test_low_energy_text(self):
        text = "I am so tired and exhausted."
        level = self.analyzer.analyze(text)
        self.assertEqual(level, EnergyLevel.LOW)

    def test_neutral_text(self):
        text = "I am going to eat lunch."
        level = self.analyzer.analyze(text)
        self.assertEqual(level, EnergyLevel.MEDIUM)

    def test_high_energy_metrics(self):
        text = "normal text"
        metrics = {'pace': 170, 'tone_valence': 0.6}
        level = self.analyzer.analyze(text, metrics)
        self.assertEqual(level, EnergyLevel.HIGH)

    def test_low_energy_metrics(self):
        text = "normal text"
        metrics = {'pace': 100, 'tone_valence': -0.6}
        level = self.analyzer.analyze(text, metrics)
        self.assertEqual(level, EnergyLevel.LOW)

    def test_mixed_signals(self):
        # Text says tired (score -2), metrics say high energy (score +2) -> 0 -> MEDIUM
        text = "I am tired"
        metrics = {'pace': 170, 'tone_valence': 0.6}
        level = self.analyzer.analyze(text, metrics)
        self.assertEqual(level, EnergyLevel.MEDIUM)

if __name__ == '__main__':
    unittest.main()
