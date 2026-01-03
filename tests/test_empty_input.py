import unittest
import subprocess
import sys

class TestEmptyInput(unittest.TestCase):
    def test_whitespace_input_behavior(self):
        """Test how the application handles whitespace-only input via args."""
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--text", "   "],
            capture_output=True,
            text=True
        )
        self.assertIn("🤔 It looks like you didn't say anything", result.stdout)

if __name__ == '__main__':
    unittest.main()
