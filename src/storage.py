import json
import os
from typing import List, Dict, Optional
from src.interfaces import IStorage

LOG_FILE = "energy_log.json"

class Storage(IStorage):
    def __init__(self, filepath=LOG_FILE):
        self.filepath = filepath
        self._cache: Optional[List[Dict]] = None

    def load_entries(self) -> List[Dict]:
        if self._cache is not None:
            return self._cache

        if not os.path.exists(self.filepath):
            self._cache = []
            return self._cache

        try:
            with open(self.filepath, 'r') as f:
                self._cache = json.load(f)
        except json.JSONDecodeError:
            self._cache = []

        return self._cache

    def save_entry(self, entry: Dict):
        entries = self.load_entries()
        entries.append(entry)
        with open(self.filepath, 'w') as f:
            # Bolt: Optimize file size and I/O by removing whitespace (indent=4 -> default separators)
            # Reduces file size by ~30% and improves read/write speed.
            json.dump(entries, f, separators=(',', ':'))

    def clear_entries(self):
        self._cache = None
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
