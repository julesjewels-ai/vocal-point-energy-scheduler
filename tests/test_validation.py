import unittest
import subprocess
import sys
import os

class TestSecurityValidation(unittest.TestCase):
    def run_cli(self, args):
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        return subprocess.run(
            [sys.executable, "src/main.py"] + args,
            capture_output=True,
            text=True,
            env=env
        )

    def test_massive_text_input_rejected(self):
        """Test that the application rejects massive text input."""
        massive_text = "a" * 100000
        result = self.run_cli(["--text", massive_text])
        self.assertEqual(result.returncode, 1, "Application should reject massive input")
        self.assertIn("Error: Input text too long", result.stdout)

    def test_invalid_pace_rejected(self):
        """Test that the application rejects invalid pace."""
        result = self.run_cli(["--text", "status", "--pace", "-50"])
        self.assertEqual(result.returncode, 1, "Application should reject negative pace")
        self.assertIn("Error: Pace must be positive", result.stdout)

    def test_invalid_tone_rejected(self):
        """Test that the application rejects invalid tone."""
        result = self.run_cli(["--text", "status", "--tone", "5.0"])
        self.assertEqual(result.returncode, 1, "Application should reject invalid tone")
        self.assertIn("Error: Tone must be between -1.0 and 1.0", result.stdout)

    def test_input_sanitization(self):
        """Test that the application sanitizes ANSI escape codes from input."""
        # \x1b[31m is RED color code, \x1b[0m is reset
        ansi_input = "\x1b[31mMalicious\x1b[0m Input"
        result = self.run_cli(["--text", ansi_input])

        # Should run successfully (return code 0) but strip the codes
        self.assertEqual(result.returncode, 0)

        # The output should contain the sanitized text (just "Malicious Input")
        # Note: The output says "Analyzing log: '...'"
        self.assertIn("Analyzing log: 'Malicious Input'", result.stdout)

        # Ensure the raw ANSI codes are NOT in the output
        self.assertNotIn("\x1b[31m", result.stdout)

if __name__ == '__main__':
    unittest.main()
