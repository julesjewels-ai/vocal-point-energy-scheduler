import json
import os
from typing import List, Dict
from src.interfaces import IStorage

LOG_FILE = "energy_log.json"

class Storage(IStorage):
    def __init__(self, filepath=LOG_FILE):
        self.filepath = filepath

    def load_entries(self) -> List[Dict]:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_entry(self, entry: Dict):
        entries = self.load_entries()
        entries.append(entry)
        with open(self.filepath, 'w') as f:
            json.dump(entries, f, indent=4)

    def clear_entries(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
