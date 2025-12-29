import sys
import argparse
from src.analyzer import EnergyAnalyzer
from src.storage import Storage
from src.feedback import FeedbackGenerator
from src.service import EnergyService

def main():
    parser = argparse.ArgumentParser(description="VocalPoint: AI Energy-Based Scheduler")
    parser.add_argument("--text", type=str, help="Simulated audio transcription log", required=False)
    parser.add_argument("--pace", type=int, help="Words per minute (default 130)", default=130)
    parser.add_argument("--tone", type=float, help="Tone valence -1.0 to 1.0 (default 0.0)", default=0.0)
    parser.add_argument("--clear", action="store_true", help="Clear all stored logs")

    args = parser.parse_args()

    # Composition Root: Assemble dependencies
    storage = Storage()
    analyzer = EnergyAnalyzer()
    feedback_gen = FeedbackGenerator()
    service = EnergyService(storage, analyzer, feedback_gen)

    if args.clear:
        service.clear_history()
        print("Energy logs cleared.")
        return

    # User Input Handling
    if args.text:
        text_input = args.text
    else:
        print("--- VocalPoint Check-In ---")
        print("Please enter your current status log (simulating audio transcription):")
        text_input = input("> ")

    metrics = {
        'pace': args.pace,
        'tone_valence': args.tone
    }

    print(f"\nAnalyzing log: '{text_input}'")

    # Delegate to Service
    energy_level = service.record_entry(text_input, metrics)
    print(f"Detected Energy Level: {energy_level.value.upper()}")

    feedback = service.get_feedback()
    print("\n--- Insight ---")
    print(feedback)

if __name__ == "__main__":
    main()
