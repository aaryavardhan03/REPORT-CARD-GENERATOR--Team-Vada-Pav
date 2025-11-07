import json
from pathlib import Path
from typing import Dict, Any, List

DB_PATH = Path(__file__).parent / "personal.json"

class StudentPersonal:
    def __init__(self):
        self.db: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}
        except json.JSONDecodeError:
            self.db = {}

    def _save(self):
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)

    def list_rolls(self) -> List[str]:
        return list(self.db.keys())

    def add_student(self, info: Dict[str, Any]) -> bool:
        roll = str(info.get('roll_no'))
        if roll in self.db:
            return False  # roll must be unique
        self.db[roll] = info
        self._save()
        return True

    def edit_student(self, roll_no: str, updates: Dict[str, Any]) -> bool:
        roll = str(roll_no)
        if roll not in self.db:
            return False
        self.db[roll].update(updates)
        self._save()
        return True

    def delete_student(self, roll_no: str) -> bool:
        roll = str(roll_no)
        if roll in self.db:
            del self.db[roll]
            self._save()
            return True
        return False

    def get_by_roll(self, roll_no: str):
        return self.db.get(str(roll_no))

    def find_by_name(self, name: str):
        name = name.strip().lower()
        matches = []
        for roll, info in self.db.items():
            if info.get('name','').strip().lower() == name:
                matches.append((roll, info))
        return matches
