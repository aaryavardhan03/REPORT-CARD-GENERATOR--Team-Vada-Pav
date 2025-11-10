# main.py
from person import get_student_info
from academic import get_academic_info
from library import get_library_info

def display_report():
    print("\n====== STUDENT INFORMATION SYSTEM ======\n")

    student = get_student_info()
    academic_data, avg, grade = get_academic_info()
    issued_books, fine = get_library_info()

    print("\n---------- STUDENT DETAILS ----------")
    for key, value in student.items():
        print(f"{key}: {value}")

    print("\n---------- ACADEMIC PERFORMANCE ----------")
    print(f"{'Subject':<20}{'Marks':<10}")
    print("-" * 30)
    for sub, mark in academic_data:
        print(f"{sub:<20}{mark:<10.2f}")
    print("-" * 30)
    print(f"Average: {avg:.2f}")
    print(f"Grade: {grade}")

    print("\n---------- LIBRARY RECORD ----------")
    if issued_books:
        print("Books Issued:")
        for b in issued_books:
            print(f" - {b}")
    else:
        print("No books issued.")
    print(f"Total Fine: ₹{fine:.2f}")

    print("\n==========================================")
    print("Student Information generated successfully!\n")

if __name__ == "__main__":
    display_report()
