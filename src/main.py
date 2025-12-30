import sys
import re
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

    # Security Enhancement: Sanitize Input
    # Remove ANSI escape codes to prevent log spoofing/terminal injection
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    text_input = ansi_escape.sub('', text_input)

    # Security Validation
    MAX_TEXT_LENGTH = 5000
    if len(text_input) > MAX_TEXT_LENGTH:
        print(f"Error: Input text too long (limit {MAX_TEXT_LENGTH} chars).")
        sys.exit(1)

    if args.pace <= 0:
        print("Error: Pace must be positive.")
        sys.exit(1)

    if not (-1.0 <= args.tone <= 1.0):
        print("Error: Tone must be between -1.0 and 1.0.")
        sys.exit(1)

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
