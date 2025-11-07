import json
from pathlib import Path
from typing import Dict, Any, List

DB_PATH = Path(__file__).parent / "library.json"

class StudentLibrary:
    def __init__(self):
        self.db: Dict[str, Dict[str, List[Dict[str,Any]]]] = {}
        self._load()

    def _load(self):
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {"current": {}, "past": {}}
        except json.JSONDecodeError:
            self.db = {"current": {}, "past": {}}

    def _save(self):
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, indent=2, ensure_ascii=False)

    def issue_book(self, roll_no: str, title: str, author: str, date_issue: str, date_submit_expected: str):
        r = str(roll_no)
        self.db.setdefault("current", {}).setdefault(r, []).append({
            "title": title, "author": author, "date_issue": date_issue, "date_submit_expected": date_submit_expected
        })
        self._save()

    def return_book(self, roll_no: str, title: str, date_submit_actual: str) -> bool:
        r = str(roll_no)
        curr = self.db.get("current", {}).get(r, [])
        for i, item in enumerate(curr):
            if item.get("title") == title:
                returned = {
                    "title": item["title"], "author": item["author"],
                    "date_issue": item["date_issue"], "date_submit_actual": date_submit_actual
                }
                self.db.setdefault("past", {}).setdefault(r, []).append(returned)
                del curr[i]
                self._save()
                return True
        return False

    def delete_current_issue(self, roll_no: str, title: str) -> bool:
        r = str(roll_no)
        curr = self.db.get("current", {}).get(r, [])
        for i, item in enumerate(curr):
            if item.get("title") == title:
                del curr[i]
                self._save()
                return True
        return False

    def get_library(self, roll_no: str):
        r = str(roll_no)
        return {
            "current": self.db.get("current", {}).get(r, []),
            "past": self.db.get("past", {}).get(r, [])
        }
