import json
from pathlib import Path
from typing import Dict, Any

DB_PATH = Path(__file__).parent / "academic.json"

class StudentAcademic:
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

    def add_exam_marks(self, roll_no: str, exam_name: str, subject_marks: Dict[str, int], max_marks_per_subject: int = 100):
        r = str(roll_no)
        self.db.setdefault(r, {"exams": {}, "max_marks_per_subject": max_marks_per_subject})
        self.db[r]["exams"][exam_name] = subject_marks
        self._save()

    def edit_exam_marks(self, roll_no: str, exam_name: str, subject_marks: Dict[str, int]) -> bool:
        r = str(roll_no)
        if r not in self.db or exam_name not in self.db[r]["exams"]:
            return False
        self.db[r]["exams"][exam_name] = subject_marks
        self._save()
        return True

    def delete_exam(self, roll_no: str, exam_name: str) -> bool:
        r = str(roll_no)
        if r in self.db and exam_name in self.db[r]["exams"]:
            del self.db[r]["exams"][exam_name]
            self._save()
            return True
        return False

    def get_academic(self, roll_no: str):
        data = self.db.get(str(roll_no))
        if not data:
            return None
        exams = data.get("exams", {})
        result = {}
        for exam, marks in exams.items():
            total = sum(marks.values())
            subjects = len(marks)
            avg = total / subjects if subjects else 0
            percentage = (total / (subjects * data.get("max_marks_per_subject",100))) * 100 if subjects else 0
            grade = self._percent_to_grade(percentage)
            result[exam] = {
                "marks": marks,
                "total": total,
                "avg_score": round(avg,2),
                "percentage": round(percentage,2),
                "grade": grade
            }
        overall_total = sum(e["total"] for e in result.values()) if result else 0
        overall_subjects = sum(len(e["marks"]) for e in result.values()) if result else 0
        overall_avg = overall_total / overall_subjects if overall_subjects else 0
        result["overall"] = {"total": overall_total, "avg_score": round(overall_avg,2)}
        return result

    def _percent_to_grade(self, p):
        if p >= 90: return "S"
        if p >= 80: return "A"
        if p >= 70: return "B"
        if p >= 60: return "C"
        if p >= 50: return "D"
        return "E"
