import sys
import argparse
from datetime import datetime
from src.analyzer import EnergyAnalyzer
from src.storage import Storage
from src.feedback import FeedbackGenerator

def main():
    parser = argparse.ArgumentParser(description="VocalPoint: AI Energy-Based Scheduler")
    parser.add_argument("--text", type=str, help="Simulated audio transcription log", required=False)
    parser.add_argument("--pace", type=int, help="Words per minute (default 130)", default=130)
    parser.add_argument("--tone", type=float, help="Tone valence -1.0 to 1.0 (default 0.0)", default=0.0)
    parser.add_argument("--clear", action="store_true", help="Clear all stored logs")

    args = parser.parse_args()

    storage = Storage()

    if args.clear:
        storage.clear_entries()
        print("Energy logs cleared.")
        return

    # If no text argument, prompt interactively
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

    analyzer = EnergyAnalyzer()
    energy_level = analyzer.analyze(text_input, metrics)
    print(f"Detected Energy Level: {energy_level.value.upper()}")

    # Save Entry
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "text": text_input,
        "metrics": metrics,
        "energy_level": energy_level.value # Store string value
    }
    storage.save_entry(new_entry)

    # Generate Feedback
    entries = storage.load_entries()
    feedback_gen = FeedbackGenerator()
    feedback = feedback_gen.generate_feedback(entries)

    print("\n--- Insight ---")
    print(feedback)

if __name__ == "__main__":
    main()
