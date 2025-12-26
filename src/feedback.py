from typing import List, Dict
from datetime import datetime
from collections import defaultdict
from src.analyzer import EnergyLevel

class FeedbackGenerator:
    def __init__(self):
        # Map EnergyLevel to numeric score
        self.score_map = {
            EnergyLevel.HIGH.value: 2,
            EnergyLevel.MEDIUM.value: 0,
            EnergyLevel.LOW.value: -2
        }

    def generate_feedback(self, entries: List[Dict]) -> str:
        count = len(entries)

        if count == 0:
            return "No energy logs found. Start logging to get insights!"

        if count < 3:
            return f"You have logged {count} entries. Keep going! specific trends will appear after 3 entries."

        # Analyze trends
        hourly_scores = defaultdict(list)

        for entry in entries:
            # entry timestamp expected in ISO format
            try:
                dt = datetime.fromisoformat(entry['timestamp'])
                hour = dt.hour
                level = entry['energy_level'] # "high", "medium", "low"

                # Check if level is enum value or string
                score = self.score_map.get(level, 0)
                hourly_scores[hour].append(score)
            except (ValueError, KeyError):
                continue

        if not hourly_scores:
            return "Could not parse entry timestamps."

        # Calculate averages
        avg_scores = {}
        for hour, scores in hourly_scores.items():
            avg_scores[hour] = sum(scores) / len(scores)

        # Identify peak and dip
        # We define peak as highest avg score, dip as lowest avg score
        if not avg_scores:
             return "Not enough data to determine trends."

        best_hour = max(avg_scores, key=avg_scores.get)
        worst_hour = min(avg_scores, key=avg_scores.get)

        best_score = avg_scores[best_hour]
        worst_score = avg_scores[worst_hour]

        feedback_lines = [f"Analysis based on {count} entries:"]

        # Format hours (e.g., 14 -> 2 PM)
        def fmt_hour(h):
            return datetime.strptime(str(h), "%H").strftime("%I %p").lstrip("0")

        if best_score > 0:
            feedback_lines.append(f"⚡ Peak Energy: You tend to feel most energetic around {fmt_hour(best_hour)}.")
        else:
            feedback_lines.append(f"⚡ Peak Energy: Your energy peaks around {fmt_hour(best_hour)}, though it's generally moderate.")

        if worst_score < 0:
            feedback_lines.append(f"💤 Low Energy: You tend to feel drained around {fmt_hour(worst_hour)}.")
        else:
            feedback_lines.append(f"💤 Low Energy: Your lowest energy point is around {fmt_hour(worst_hour)}.")

        return "\n".join(feedback_lines)
