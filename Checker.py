import numpy as np

# This is a checker for HR_Basic many to one gale shapley matching
def check(matching, hospitals, students):
    students_prefs = {student: list(prefs) for student, prefs in students.items()}
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}
    for hospital in matching:
        list_of_students = matching[hospital]  # Students in the hospital in the match
        hospital_prefs = hospitals_prefs[hospital]
        hospital_student_indices=[hospital_prefs.index(student) for student in list_of_students if student!="x"]
        max_student_index=-1
        if len(hospital_student_indices)==0:
            max_student_index=np.inf
        else:
            max_student_index = np.max(hospital_student_indices)  # Least pref
        # student in hospital
        for student in hospital_prefs:  # If a student of lower pref takes his place or there's room, check student
            # pref, maybe there's a block
            if ((hospital in students_prefs[student]) and (student not in list_of_students and hospital_prefs.index(student) < max_student_index or (
                    "x" in matching[hospital]))):
                student_hospital = -1
                for hosp in matching:
                    if student in matching[hosp]:
                        student_hospital = hosp
                        continue
                if student_hospital == -1 or hospital not in students_prefs[student]:
                    print(str(student)+" has no hospital, and "+str(hospital)+" wants him")
                    return False  # Student has no hospital, and this hospital wants him
                if students_prefs[student].index(student_hospital) > students_prefs[student].index(hospital):
                    print(str(student) + " is in "+str(student_hospital)+" and " + str(hospital) + "wants him, and he "
                                                                                                   "prefers them too")
                    return False  # Student has an hospital but rather have this one in question
    return True  # No blocks
