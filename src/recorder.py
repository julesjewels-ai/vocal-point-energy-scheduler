import threading
import wave
import struct
import os
import time

try:
    from pvrecorder import PvRecorder
    PV_RECORDER_AVAILABLE = True
except ImportError:
    PV_RECORDER_AVAILABLE = False

class AudioRecorder:
    def __init__(self, output_filename="input.wav", device_index=-1, frame_length=512):
        self.output_filename = output_filename
        self.device_index = device_index
        self.frame_length = frame_length
        self.is_recording = False
        self._frames = []
        self._mock_mode = not PV_RECORDER_AVAILABLE

        # Check if we are in an environment with no devices (like CI/Server) even if library is available
        if PV_RECORDER_AVAILABLE:
            try:
                devices = PvRecorder.get_available_devices()
                if not devices or (len(devices) == 1 and "Discard" in devices[0]):
                     # Likely a dummy device, fallback to mock if preferred, or allow it but warn.
                     # For this implementation, we will use mock mode if no useful devices are found
                     # to prevent crashing on "start()"
                     pass
            except Exception:
                self._mock_mode = True

    def _record_loop(self, recorder):
        while self.is_recording:
            try:
                frame = recorder.read()
                self._frames.extend(frame)
            except Exception as e:
                print(f"Error reading audio frame: {e}")
                break

    def _mock_record_loop(self):
        """Generates silence/dummy data for testing."""
        while self.is_recording:
            time.sleep(0.03) # Approx 32ms for 512 samples at 16kHz
            # Generate 512 samples of silence (0)
            self._frames.extend([0] * self.frame_length)

    def record_audio(self):
        """
        Records audio until the user presses Enter.
        Saves to self.output_filename.
        """
        print(f"🎙️  Recording... Press ENTER to stop.")

        self.is_recording = True
        self._frames = []

        if self._mock_mode:
            print("⚠️  (Mock Mode: simulating recording)")
            recording_thread = threading.Thread(target=self._mock_record_loop)
            recording_thread.start()
        else:
            try:
                recorder = PvRecorder(device_index=self.device_index, frame_length=self.frame_length)
                recorder.start()
                recording_thread = threading.Thread(target=self._record_loop, args=(recorder,))
                recording_thread.start()
            except Exception as e:
                print(f"❌ Error initializing recorder: {e}")
                self.is_recording = False
                return

        # Wait for user input to stop
        try:
            input()
        except KeyboardInterrupt:
            pass
        finally:
            self.is_recording = False
            recording_thread.join()

            if not self._mock_mode:
                recorder.stop()
                recorder.delete()

        self._save_to_wav()
        print(f"💾 Recording saved to {self.output_filename}")

    def _save_to_wav(self):
        if not self._frames:
            return

        with wave.open(self.output_filename, 'w') as f:
            f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
            f.writeframes(struct.pack("h" * len(self._frames), *self._frames))
