import unittest
import subprocess
import sys
import os

class TestUXInteraction(unittest.TestCase):
    def test_empty_interactive_input_handled_gracefully(self):
        """Test that empty input in interactive mode is handled gracefully without processing."""
        # Run main.py with empty input piped to stdin
        result = subprocess.run(
            [sys.executable, "src/main.py"],
            input="\n",  # Simulate hitting Enter immediately
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": os.getcwd()}
        )

        # We expect a graceful exit, so return code 0
        self.assertEqual(result.returncode, 0)

        # We expect a warning message
        self.assertIn("⚠️  No text entered.", result.stdout)

        # We expect IT DID NOT proceed to analysis
        self.assertNotIn("🔍 Analyzing log:", result.stdout)
        self.assertNotIn("✨ Detected Energy Level:", result.stdout)

if __name__ == '__main__':
    unittest.main()
