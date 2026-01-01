import unittest
import subprocess
import sys
import os

class TestEmptyInput(unittest.TestCase):
    def test_empty_input_behavior(self):
        """Test updated empty input behavior."""
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()

        # Simulate empty input via stdin
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            input="\n", # Simulate pressing Enter immediately
            capture_output=True,
            text=True,
            env=env
        )

        # Now it should exit gracefully (0) but with our specific message
        self.assertEqual(result.returncode, 0)
        self.assertIn("It looks like you didn't say anything", result.stdout)
        self.assertNotIn("Detected Energy Level:", result.stdout)

    def test_whitespace_input_behavior(self):
        """Test updated whitespace input behavior."""
        env = os.environ.copy()
        env['PYTHONPATH'] = os.getcwd()

        result = subprocess.run(
            [sys.executable, "src/main.py"],
            input="   \n",
            capture_output=True,
            text=True,
            env=env
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("It looks like you didn't say anything", result.stdout)
        self.assertNotIn("Detected Energy Level:", result.stdout)

if __name__ == '__main__':
    unittest.main()
