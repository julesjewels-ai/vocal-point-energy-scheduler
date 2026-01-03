import unittest
import os
import threading
import time
from unittest.mock import MagicMock, patch
from src.recorder import AudioRecorder

class TestAudioRecorder(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_audio.wav"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_init(self):
        recorder = AudioRecorder(output_filename=self.test_file)
        self.assertEqual(recorder.output_filename, self.test_file)
        self.assertFalse(recorder.is_recording)

    @patch('builtins.input', side_effect=['']) # Simulate user pressing Enter immediately
    @patch('src.recorder.PvRecorder') # Mock PvRecorder if it tries to import
    def test_record_mock_mode(self, mock_pv_recorder, mock_input):
        # Force mock mode
        recorder = AudioRecorder(output_filename=self.test_file)
        recorder._mock_mode = True

        # We need to simulate that recording actually happens for a split second
        # The input() mock returns immediately, so the thread might not have run much.
        # However, the logic should still produce a valid (empty or small) wav file.

        recorder.record_audio()

        self.assertTrue(os.path.exists(self.test_file))
        # Check if file has header at least
        self.assertGreater(os.path.getsize(self.test_file), 0)

    @patch('builtins.input', side_effect=[''])
    def test_save_to_wav_content(self, mock_input):
        recorder = AudioRecorder(output_filename=self.test_file)
        # Manually populate frames
        recorder._frames = [0] * 1024 # Some dummy data
        recorder._save_to_wav()

        self.assertTrue(os.path.exists(self.test_file))
        self.assertGreater(os.path.getsize(self.test_file), 1024)

if __name__ == '__main__':
    unittest.main()
