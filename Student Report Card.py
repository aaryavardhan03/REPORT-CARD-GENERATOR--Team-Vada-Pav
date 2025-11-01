import re

print("===== Report Card Generator =====")

def is_valid_name(text):
    return text.replace(" ", "").isalpha()

while True:
    name = input("Enter the student's name: ")
    if not is_valid_name(name):
        print(" ERROR : Invalid name! The student's name cannot contain numbers or special characters. Please re-enter.")
    else:
        break

roll_pattern = r"^\d{2}[A-Z]{3}\d{4}$"
while True:
    roll_no = input("Enter the roll number : ")
    if re.match(roll_pattern, roll_no):
        break
    else:
        print("ERROR :  Invalid roll number format! Please follow the format (e.g. 23ABC2025).")

while True:
    try:
        n = int(input("Enter the number of subjects: "))
        if n <= 0:
            print(" ERROR : Number of subjects must be positive. Please re-enter.")
            continue
        break
    except ValueError:
        print(" ERROR : You entered a letter instead of a number! Please enter a valid number of subjects.")

subjects = {}

for i in range(n):
    while True:
        subject = input(f"\nEnter name of subject {i+1}: ")
        if not is_valid_name(subject):
            print("ERROR :  Invalid subject name! Subject names cannot contain numbers or special characters.")
        else:
            break

    while True:
        total_input = input(f"Enter total marks for {subject}: ")
        if not total_input.replace('.', '', 1).isdigit():
            print("ERROR :  You entered a letter instead of a number! Please enter a numeric value.")
            continue
        total = float(total_input)
        if total < 0:
            print("ERROR :  Total marks cannot be negative. Please re-enter.")
            continue
        break

    while True:
        obtained_input = input(f"Enter marks obtained in {subject}: ")
        if not obtained_input.replace('.', '', 1).isdigit():
            print(" ERROR :  You entered a letter instead of a number! Please enter a numeric value.")
            continue
        obtained = float(obtained_input)
        if obtained < 0:
            print(" ERROR :  Marks cannot be negative. Please re-enter.")
            continue
        elif obtained > total:
            print(" ERROR : Obtained marks cannot be greater than total marks. Please re-enter.")
            continue
        break

    subjects[subject] = {"obtained": obtained, "total": total}

total_obtained = sum(info["obtained"] for info in subjects.values())
total_max = sum(info["total"] for info in subjects.values())
average_percentage = (total_obtained / total_max) * 100 if total_max > 0 else 0

if average_percentage >= 95:
    grade = 'S'
elif average_percentage >= 90:
    grade = 'A'
elif average_percentage >= 80:
    grade = 'B'
elif average_percentage >= 70:
    grade = 'C'
elif average_percentage >= 60:
    grade = 'D'
elif average_percentage >= 50:
    grade = 'E'
else:
    grade = 'F'

print("\n===== REPORT CARD =====")
print(f"Name       : {name}")
print(f"Roll Number: {roll_no}")
print("----------------------------")
print(f"{'Subject':<15}{'Marks':>10}{'Out of':>10}{'Percent':>12}")
print("-" * 47)

for subject, info in subjects.items():
    percent = (info["obtained"] / info["total"]) * 100 if info["total"] > 0 else 0
    print(f"{subject:<15}{info['obtained']:>10.1f}{info['total']:>10.1f}{percent:>11.2f}%")

print("-" * 47)
print(f"Total Marks : {total_obtained:.1f} / {total_max}")
print(f"Average     : {average_percentage:.2f}%")
print(f"Grade       : {grade}")
print("============================")
