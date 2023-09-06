# This is EMVW algo. The same as HR_Basic but takes in already a matching in the making.

# ??? Student that was in a hospital and then left and is now without a match, will have his ORIGINAL pref
import numpy as np


# the matching I get is a match for a sub group of all students.
def emvw2(students, hospitals, capacities, matching, sub_singles):
    # if matching empty? I think it's ok, only time complexity wise

    # This is to handle a pre-match given

    # Make copies of the preference lists so that we can remove elements from them

    # old_students_prefs = {student: list(prefs) for student, prefs in students.items()}
    # old_hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}
    students_prefs = {student: list(prefs) for student, prefs in students.items()}

    # List of unmatched students in the current matching
    unmatched_students = set(students)

    # List of students who didn't get any match.
    single_students = set()

    for single in sub_singles:  # They will stay single
        unmatched_students.remove(single)
        single_students.add(single)

    # Cut pref lists

    for hospital in matching:  # Hospital in match
        hospital_students = list(filter(lambda a: a != "x", matching[hospital]))  # Students in match
        if len(hospital_students) == 0:
            continue
        if capacities[hospital] == len(hospital_students):  # Hospital is in full cap.
            student_indice = np.max([hospitals_prefs[hospital].index(x) for x in hospital_students])  # Student
            # max placement in hospitals' pref
            hospitals_prefs[hospital] = hospitals_prefs[hospital][
                                        0:student_indice + 1]  # Cut all hospitals before the matched
            # student in the hospitals' pref list
        for i in hospital_students:
            hospital_indice = students_prefs[i].index(hospital)  # Hospital placement in students' pref
            students_prefs[i] = students_prefs[i][hospital_indice:]  # Cut all hospitals
            # better than the matched hospital in the students' pref list
            unmatched_students.remove(i)  # Remove student from unmatched students

    hospital_capacities = {hospital: capacity for hospital, capacity in capacities.items()}
    # In case the pre-match is NOT in MY template (X's for no entries, capacity size array)
    # ?

    # ?
    # This counters the number of students currently assigned to each hospital
    hospital_counters = {hospital: 0 for hospital in capacities.keys()}
    for hosp in hospital_counters:
        if hosp in matching:
            hospital_counters[hosp] = len(matching[hosp]) - matching[hosp].count("x")
            # print(hospital_counters[hosp])

    # From here it's like before
    # What we have: student pref lists were cut using the matched hospitals' index (inclusive)
    # Hospital pref lists were cut using the MINIMAL indice of his matched students (inclusive)

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
            for i in range(hospital_capacities[hospital] - 2, chosen_index-1,-1):
                matching[hospital][i + 1] = matching[hospital][i]
            matching[hospital][chosen_index] = student
            unmatched_students.remove(student)

    return matching, single_students

def emvw(students, hospitals, capacities, matching, sub_singles):
    # if matching empty? I think it's ok, only time complexity wise

    # This is to handle a pre-match given

    # Make copies of the preference lists so that we can remove elements from them

    # old_students_prefs = {student: list(prefs) for student, prefs in students.items()}
    # old_hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}
    students_prefs = {student: list(prefs) for student, prefs in students.items()}

    # List of unmatched students in the current matching
    unmatched_students = set(students)

    # List of students who didn't get any match.
    single_students = set()

    for single in sub_singles:  # They will stay single
        unmatched_students.remove(single)
        single_students.add(single)

    # Cut pref lists

    for hospital in matching:  # Hospital in match
        hospital_students = list(filter(lambda a: a != "x", matching[hospital]))  # Students in match
        if len(hospital_students) == 0:
            continue
        if capacities[hospital] == len(hospital_students):  # Hospital is in full cap.
            student_indice = np.max([hospitals_prefs[hospital].index(x) for x in hospital_students])  # Student
            # max placement in hospitals' pref
            hospitals_prefs[hospital] = hospitals_prefs[hospital][
                                        0:student_indice + 1]  # Cut all hospitals before the matched
            # student in the hospitals' pref list
        for i in hospital_students:
            hospital_indice = students_prefs[i].index(hospital)  # Hospital placement in students' pref
            students_prefs[i] = students_prefs[i][hospital_indice:]  # Cut all hospitals
            # better than the matched hospital in the students' pref list
            unmatched_students.remove(i)  # Remove student from unmatched students

    hospital_capacities = {hospital: capacity for hospital, capacity in capacities.items()}
    # In case the pre-match is NOT in MY template (X's for no entries, capacity size array)
    # ?

    # ?
    # This counters the number of students currently assigned to each hospital
    hospital_counters = {hospital: 0 for hospital in capacities.keys()}
    for hosp in hospital_counters:
        if hosp in matching:
            hospital_counters[hosp] = len(matching[hosp]) - matching[hosp].count("x")
            # print(hospital_counters[hosp])

    # From here it's like before
    # What we have: student pref lists were cut using the matched hospitals' index (inclusive)
    # Hospital pref lists were cut using the MINIMAL indice of his matched students (inclusive)

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
            hospital_prefs = hospitals_prefs[hospital]
            if student not in hospitals_prefs[hospital]:
                continue
            #
            # Hospital is not full capacity, and student is in it's pref, so it accepts the proposal

            chosen_index = -1
            for i in range(0,hospital_counters[hospital]):
                hospital_prefs_index_of_student = hospital_prefs.index(student)
                if hospital_prefs_index_of_student < hospital_prefs.index(matching[hospital][i]):
                    chosen_index = i
                    break
            if chosen_index == -1: # Put last
                matching[hospital][hospital_counters[hospital]] = student
            else:
                for i in range(hospital_counters[hospital] - 1, chosen_index - 1, -1):
                    matching[hospital][i + 1] = matching[hospital][i]
                matching[hospital][chosen_index] = student
            hospital_counters[hospital] = 1 + hospital_counters[hospital]

            unmatched_students.remove(student)
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
            for i in range(hospital_capacities[hospital] - 2, chosen_index-1,-1):
                matching[hospital][i + 1] = matching[hospital][i]
            matching[hospital][chosen_index] = student
            unmatched_students.remove(student)

    return matching, single_students