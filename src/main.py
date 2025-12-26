import sys
import argparse
from src.analyzer import EnergyAnalyzer
from src.calendar_api import Calendar
from src.scheduler import Scheduler

def main():
    parser = argparse.ArgumentParser(description="VocalPoint: AI Energy-Based Scheduler")
    parser.add_argument("--text", type=str, help="Simulated audio transcription log", required=False)
    parser.add_argument("--pace", type=int, help="Words per minute (default 130)", default=130)
    parser.add_argument("--tone", type=float, help="Tone valence -1.0 to 1.0 (default 0.0)", default=0.0)

    args = parser.parse_args()

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
    print(f"Metrics: {metrics}")

    analyzer = EnergyAnalyzer()
    energy_level = analyzer.analyze(text_input, metrics)
    print(f"Detected Energy Level: {energy_level.value.upper()}")

    calendar = Calendar()
    tasks = calendar.get_tasks()

    scheduler = Scheduler()
    recommendation = scheduler.get_recommendation(tasks, energy_level)
    print(f"\nRecommendation: {recommendation}")

    sorted_tasks = scheduler.schedule_tasks(tasks, energy_level)
    print("\nSuggested Schedule:")
    for i, task in enumerate(sorted_tasks):
        print(f"{i+1}. [{task.required_energy.value.upper()}] {task.title} ({task.duration_minutes} min)")

if __name__ == "__main__":
    main()
