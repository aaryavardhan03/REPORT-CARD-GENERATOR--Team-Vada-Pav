import pprint
from typing import List

def colify(rows: List[List[str]], headers: List[str]) -> str:
    if not rows:
        widths = [len(h) for h in headers]
        header = " | ".join(h.ljust(widths[i]) for i,h in enumerate(headers))
        sep = "-+-".join("-"*w for w in widths)
        return header + "\n" + sep
    widths = [max(len(str(h)), *(len(str(r[i])) for r in rows)) for i,h in enumerate(headers)]
    header = " | ".join(h.ljust(widths[i]) for i,h in enumerate(headers))
    sep = "-+-".join("-"*w for w in widths)
    lines = [header, sep] + [" | ".join(str(r[i]).ljust(widths[i]) for i in range(len(headers))) for r in rows]
    return "\n".join(lines)

def pretty_personal(info):
    if not info: return "No personal info found."
    rows = []
    for k in ("name","class","roll_no","section","area_of_study","hometown"):
        rows.append([k.capitalize(), info.get(k,"")])
    parents = info.get("parents",{})
    parent_str = "Father: " + parents.get("father","") + "  |  Mother: " + parents.get("mother","")
    rows.append(["Parents", parent_str])
    return colify(rows, ["Field","Value"])

def pretty_library(lib):
    if not lib: return "No library records."
    out = []
    curr = lib.get("current",[])
    past = lib.get("past",[])
    out.append("=== CURRENT ISSUES ===")
    if curr:
        rows = [[i.get("title",""), i.get("author",""), i.get("date_issue",""), i.get("date_submit_expected","")] for i in curr]
        out.append(colify(rows, ["Title","Author","Date Issue","Expected Submit"]))
    else:
        out.append("(none)")
    out.append("")
    out.append("=== PAST ISSUES ===")
    if past:
        rows = [[i.get("title",""), i.get("author",""), i.get("date_issue",""), i.get("date_submit_actual","")] for i in past]
        out.append(colify(rows, ["Title","Author","Date Issue","Date Returned"]))
    else:
        out.append("(none)")
    return "\n".join(out)

def pretty_academic_reportcard(acad):
    if not acad: return "No academic records."
    parts = []
    for exam, data in acad.items():
        if exam=="overall": continue
        parts.append(f"----- {exam.upper()} -----")
        marks = data.get("marks",{})
        rows = [[s,str(marks[s])] for s in marks]
        parts.append(colify(rows, ["Subject","Marks"]))
        parts.append(f"Total: {data.get('total')}    Avg: {data.get('avg_score')}    Perc: {data.get('percentage')}%    Grade: {data.get('grade')}")
        parts.append("\n")
    overall = acad.get("overall",{})
    if overall:
        parts.append("----- OVERALL -----")
        parts.append(f"Overall Total: {overall.get('total')}    Overall Avg: {overall.get('avg_score')}")
    return "\n".join(parts)

def choose_student(sp):
    q = input("Search by (1) Roll no or (2) Name? Enter 1 or 2: ").strip()
    if q=='1': return input("Enter roll no: ").strip()
    name = input("Enter full name: ").strip()
    matches = sp.find_by_name(name)
    if not matches:
        print("No student found with that name."); return None
    if len(matches)>1:
        print("Multiple matches - please use roll no.");
        for r,info in matches: print(r, info.get("name"), info.get("hometown",""))
        return None
    return matches[0][0]

def display_menu(sp, sa, sl):
    while True:
        print("\nModules: personal / academic / library / exit")
        mod = input("Choose module: ").strip().lower()
        if mod=="exit": break
        roll = choose_student(sp)
        if not roll: continue
        if mod=="personal":
            act = input("Action (view/add/edit/delete): ").strip().lower()
            if act=="view":
                print(pretty_personal(sp.get_by_roll(roll)))
            elif act=="add":
                name = input("Name: ")
                cls = input("Class: ")
                father = input("Father's name: ")
                mother = input("Mother's name: ")
                hometown = input("Hometown: ")
                section = input("Section: ")
                area = input("Area of study: ")
                info = {'roll_no':roll,'name':name,'class':cls,'parents':{'father':father,'mother':mother},'hometown':hometown,'section':section,'area_of_study':area}
                print('Added' if sp.add_student(info) else 'Roll exists')
            elif act=="edit":
                k = input('Field to update: ')
                if k=='parents':
                    father = input("Father's name: "); mother = input("Mother's name: ")
                    v = {'father':father,'mother':mother}
                else:
                    v = input('New value: ')
                print('Updated' if sp.edit_student(roll,{k:v}) else 'No such student')
            elif act=="delete":
                print('Deleted' if sp.delete_student(roll) else 'No such student')
        elif mod=="academic":
            act = input("Action (view/add/edit/delete): ").strip().lower()
            if act=="view":
                print(pretty_academic_reportcard(sa.get_academic(roll)))
            elif act in ("add","edit"):
                exam = input("Exam name: ")
                subs = input("subjects as s1:m1,s2:m2: ")
                subject_marks = dict((s.split(':')[0], int(s.split(':')[1])) for s in subs.split(',') if ':' in s)
                if act=="add":
                    sa.add_exam_marks(roll, exam, subject_marks)
                else:
                    print('Edited' if sa.edit_exam_marks(roll,exam,subject_marks) else 'Failed')
            elif act=="delete":
                exam = input("Exam name to delete: ")
                print('Deleted' if sa.delete_exam(roll,exam) else 'Failed')
        elif mod=="library":
            act = input("Action (view/issue/return/delete): ").strip().lower()
            if act=="view":
                print(pretty_library(sl.get_library(roll)))
            elif act=="issue":
                title = input("Title: ")
                author = input("Author: ")
                date_issue = input("Date issue (YYYY-MM-DD): ")
                date_submit_expected = input("Expected submit (YYYY-MM-DD): ")
                sl.issue_book(roll,title,author,date_issue,date_submit_expected)
                print("Book issued")
            elif act=="return":
                title = input("Title to return: ")
                date_actual = input("Return date (YYYY-MM-DD): ")
                print('Returned' if sl.return_book(roll,title,date_actual) else 'Not found')
            elif act=="delete":
                title = input("Title to delete: ")
                print('Deleted' if sl.delete_current_issue(roll,title) else 'Not found')
        else:
            print("Unknown module")
