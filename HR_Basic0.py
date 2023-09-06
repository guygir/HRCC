def gale_shapley0(students, hospitals):
    # Make copies of the preference lists so that we can remove elements from them
    students_prefs = {student: list(prefs) for student, prefs in students.items()}
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}

    # Each student is initially unmatched
    unmatched_students = set(students)
    # The matching is initially empty
    matching = {}

    while unmatched_students:
        student = next(iter(unmatched_students))

        # This is added to handle the case where students CAN stay unmatched (capacity/hospital pref reasons)
        if len(students_prefs[student]) == 0:
            unmatched_students.remove(student)
            continue
        #

        # Student's next pref hospital
        hospital = students_prefs[student].pop(0)
        # This is to handle partial order of students in the hospital pref
        if student not in hospitals_prefs[hospital]:
            continue
        #

        fiance = matching.get(hospital)
        if not fiance:
            # Hospital is not matched, and student is in it's pref, so it accepts the proposal
            matching[hospital] = student
            unmatched_students.remove(student)
        else:
            # Hospital is already matched, so it compares the two students
            hospital_prefs = hospitals_prefs[hospital]
            if hospital_prefs.index(student) < hospital_prefs.index(fiance):
                # Hospital prefers the new student, so it breaks off the matching and accepts the new student instead
                matching[hospital] = student
                unmatched_students.add(fiance)
                unmatched_students.remove(student)
    return matching
