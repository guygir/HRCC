# Here I return unmatched students list too
def gale_shapley(students, hospitals, capacities):
    # Make copies of the preference lists so that we can remove elements from them
    students_prefs = {student: list(prefs) for student, prefs in students.items()}
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}
    hospital_capacities = {hospital: capacity for hospital, capacity in capacities.items()}
    # This counters the number of students currently assigned to each hospital
    hospital_counters = {hospital: 0 for hospital in capacities.keys()}
    # Each student is initially unmatched
    unmatched_students = set(students)
    # The matching is initially empty
    matching = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    # X MEANS NO MATCHING. we return ["x"] as no students matched.

    # List of students who didn't get any match.
    single_students=set()

    while unmatched_students:
        student = next(iter(unmatched_students))

        # This is added to handle the case where students CAN stay unmatched (capacity/hospital pref reasons)
        if len(students_prefs[student]) == 0:
            unmatched_students.remove(student)
            single_students.add(student)
            continue
        #
        # Student's next pref hospital
        hospital = students_prefs[student].pop(0)
        fiance = matching.get(hospital)
        # If hospital capacity isn't full
        if hospital_capacities.get(hospital) > hospital_counters.get(hospital):
            # This is to handle partial order of students in the hospital pref
            if student not in hospitals_prefs[hospital]:
                continue
            #
            # Hospital is not full capacity, and student is in it's pref, so it accepts the proposal
            matching[hospital][hospital_counters[hospital]] = student
            unmatched_students.remove(student)
            hospital_counters[hospital] = 1 + hospital_counters[hospital]
        else:
            # Hospital is already full capacity, so it check the pref index of the student
            hospital_prefs = hospitals_prefs[hospital]
            # This is to handle partial order of students in the hospital pref
            if student not in hospital_prefs:
                continue
            #
            chosen_index = -1
            for i in range(0, hospital_capacities[hospital]):
                hospital_prefs_index_of_student = hospital_prefs.index(student)
                if hospital_prefs_index_of_student < hospital_prefs.index(matching[hospital][i]):
                    chosen_index = i
                    break
            if chosen_index == -1:
                continue  # Hospital doesn't want student, all of its other students are better
            # If we got here, new student is better than all students in the hospital with index i or higher (which
            # means they're worse), so remove last student in the hospital, shift the rest and add the new student in
            # the correct place.
            unmatched_students.add(matching[hospital][hospital_capacities[hospital] - 1])
            '''
            for i in range(chosen_index, hospital_capacities[hospital] - 1):
                matching[hospital][i + 1] = matching[hospital][i] # THIS IS WRONG AND FIXED IN EMVW
            '''
            for i in range(hospital_capacities[hospital] - 2, chosen_index-1,-1):
                matching[hospital][i + 1] = matching[hospital][i]

            matching[hospital][chosen_index] = student
            unmatched_students.remove(student)

    return matching,single_students
