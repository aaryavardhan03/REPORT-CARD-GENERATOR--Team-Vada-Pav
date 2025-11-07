from personal import StudentPersonal
from academic import StudentAcademic
from library import StudentLibrary
from ui import display_menu

sp,sa,sl = StudentPersonal(),StudentAcademic(),StudentLibrary()

if __name__ =='__main__':
    display_menu(sp,sa,sl)
