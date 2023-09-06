# Here I return unmatched students list too
import numpy as np

# IS IT IMPORTANT IF THEY GO 1 BY 1?
def reversed_gale_shapley(students, hospitals, capacities):
    # Hospitals offer to students. They offer to 1 by 1, not to #capacity. I think it's esaier to look at.

    # Make copies of the preference lists so that we can remove elements from them
    students_prefs = {student: list(prefs) for student, prefs in students.items()}
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}
    hospital_capacities = {hospital: capacity for hospital, capacity in capacities.items()}
    # This counters the number of students currently assigned to each hospital
    hospital_counters = {hospital: 0 for hospital in capacities.keys()}
    # This will have the hospitals who we dont need to go through anymore
    unfinished_hospitals = set(hospitals)
    # The matching is initially empty
    matching = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    # X MEANS NO MATCHING. we return ["x"] as no students matched.

    # Current hospital for each student
    current_hospital = {student: "x" for student in students}

    while unfinished_hospitals:
        hospital = next(iter(unfinished_hospitals))
        # This is where the hospital went through his entire list or his capacity is full
        if len(hospitals_prefs[hospital]) == 0 or capacities[hospital] == hospital_counters[hospital]:
            unfinished_hospitals.remove(hospital)
            continue
        #
        # Hospital's next pref student
        student = hospitals_prefs[hospital].pop(0)
        fiance = current_hospital.get(student)
        if (hospital not in students_prefs[student]):
            continue
        if fiance == "x":
            fiance_indice = np.inf
        else:
            fiance_indice = students_prefs[student].index(fiance)
        hospital_indice = students_prefs[student].index(hospital)

        if (hospital_indice < fiance_indice):  # Student prefs to switch hospitals!
            prev_hospital = current_hospital[student]
            if prev_hospital!= "x":
                if prev_hospital not in unfinished_hospitals:  # That's a set so maybe I dont need this
                    unfinished_hospitals.add(prev_hospital)
                # Fix prev_hospital matching by moving the students
                #print(prev_hospital,student,fiance_indice,fiance)
                removed_student_indice = matching[prev_hospital].index(student)
                for i in range(removed_student_indice, hospital_counters[prev_hospital] - 1):
                    if matching[prev_hospital][i + 1] == "x":  # The rest are X's
                        break
                    matching[prev_hospital][i] = matching[prev_hospital][i + 1]
                matching[prev_hospital][hospital_counters[prev_hospital] - 1] = "x"  # Put x in last. Maybe not need
                #
                # Reduce country by 1 for prev hospital, and rest is for the new hospital
                hospital_counters[prev_hospital] = hospital_counters[prev_hospital] - 1

            current_hospital[student] = hospital
            matching[hospital][hospital_counters[hospital]] = student
            hospital_counters[hospital] = 1 + hospital_counters[hospital]

        '''
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
            for i in range(chosen_index, hospital_capacities[hospital] - 1):
                matching[hospital][i + 1] = matching[hospital][i]
            matching[hospital][chosen_index] = student
            unmatched_students.remove(student)
            '''

    # List of students who didn't get any match.
    single_students = {student for student, x in current_hospital.items() if x == "x"}

    return matching, single_students, current_hospital
