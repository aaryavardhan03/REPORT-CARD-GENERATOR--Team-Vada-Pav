# academic.py
import math

def calculate_grade(avg):
    """Return grade based on average marks."""
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

def get_academic_info():
    """Take subject details, calculate average and grade."""
    subjects = []
    marks = []

    n = int(input("Enter number of subjects: "))

    for i in range(n):
        subject = input(f"Enter subject {i+1} name: ")
        mark = float(input(f"Enter marks obtained in {subject} (out of 100): "))
        subjects.append(subject.title())
        marks.append(mark)

    avg = sum(marks) / n
    grade = calculate_grade(avg)

    academic_data = list(zip(subjects, marks))
    return academic_data, avg, grade
