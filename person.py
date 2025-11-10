# person.py
import re

def validate_name(name):
    """Check if name contains only alphabets and spaces."""
    return bool(re.match(r"^[A-Za-z\s]+$", name))

def get_student_info():
    """Get and validate basic student details."""
    name = input("Enter student name: ")
    while not validate_name(name):
        name = input("Invalid name. Please enter only alphabets: ")

    roll_no = input("Enter roll number: ")
    dept = input("Enter department: ")

    return {"Name": name.title(), "Roll No": roll_no, "Department": dept}
