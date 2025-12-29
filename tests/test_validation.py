import unittest
import subprocess
import sys

class TestSecurityValidation(unittest.TestCase):
    def test_massive_text_input_rejected(self):
        """Test that the application rejects massive text input."""
        massive_text = "a" * 100000
        result = subprocess.run(
            [sys.executable, "src/main.py", "--text", massive_text],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1, "Application should reject massive input")
        self.assertIn("Error: Input text too long", result.stdout)

    def test_invalid_pace_rejected(self):
        """Test that the application rejects invalid pace."""
        result = subprocess.run(
            [sys.executable, "src/main.py", "--text", "status", "--pace", "-50"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1, "Application should reject negative pace")
        self.assertIn("Error: Pace must be positive", result.stdout)

    def test_invalid_tone_rejected(self):
        """Test that the application rejects invalid tone."""
        result = subprocess.run(
            [sys.executable, "src/main.py", "--text", "status", "--tone", "5.0"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 1, "Application should reject invalid tone")
        self.assertIn("Error: Tone must be between -1.0 and 1.0", result.stdout)

if __name__ == '__main__':
    unittest.main()
