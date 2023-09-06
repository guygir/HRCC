import numpy as np
from EMVW import emvw
from Reversed_HR import reversed_gale_shapley
from Checker import check

# unoptimal_match =/= best match for hospitals. student is one such that his match is different than the match in the
# matching which is best for hospitals. optimal_student_to_hospital is to check validation (from REVERSED). Hospital
# prefs is the ongoing prefs. I want to change the pref lists of hospital and it will stay later on (for the big BM
# algo)
def BM(unoptimal_matching, student, optimal_student_to_hospital, hospitals_prefs):
    kicked_students = set()  # newly kicked students from the non optimal hospital

    optimal_hospital = optimal_student_to_hospital[student]  # Could be x
    current_hospital = \
        [hospital for hospital, list_of_students in unoptimal_matching.items() if student in list_of_students][
            0]  # This can be done quicker if I implement student:hospital in HR_Basic like I did in EMVW. Finds the
    # students' hospital in the unoptimal (hospital wise) matching
    if optimal_hospital == current_hospital:  # Validation
        print("Student already in the hospital that is in the hospital optimal matching")
        return False
    # Current hospital can be X AND we get here.
    hospital_pref = hospitals_prefs[current_hospital]
    hospital_match = unoptimal_matching[current_hospital]
    student_indice_in_current_pref = hospital_pref.index(student)
    student_indice_in_current_match = hospital_match.index(
        student)  # We assume the order in the matching is like the ranking of the preference! Otherwise we need to
    # go over all pref instead and do one by one
    for i in range(student_indice_in_current_match,
                   len(hospital_match)):  # Now we go over all students that are at students' index or higher.
        kicked_student = hospital_match[i]
        if kicked_student == "x":
            continue
        hospital_match[i] = "x"
        kicked_students.add(kicked_student)
    # Kicked all worse students from the current hospital
    hospital_pref_new = hospital_pref[0:student_indice_in_current_pref]
    # TO RUN EMVW AGAIN DO I NEED SUB MATCH??
    hospitals_prefs[current_hospital] = hospital_pref_new
    unoptimal_matching[current_hospital] = hospital_match

    return hospitals_prefs, unoptimal_matching, kicked_students


def check_for_optimal(students, optimal_student_to_hospital,
                      match, singles_in_match):  # Return x if optimal, student name if not (for him)
    for student in students:
        opt_hospital = optimal_student_to_hospital[student]
        if opt_hospital=="x":
            if student in singles_in_match:
                continue
            else:
                return student
        if student not in match[opt_hospital]:
            return student
    return "x"

# I work on a copy of the hospitals prefs. The original isn't changed.
def opt_students_to_opt_hospitals(students, hospitals, capacities):
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()} # COPY!
    empty_match = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    empty_sub_singles = set()
    matching, singles = emvw(students, hospitals_prefs, capacities, empty_match, empty_sub_singles)
    optimal_matching, optimal_singles, optimal_student_to_hospital = reversed_gale_shapley(students, hospitals_prefs,
                                                                                           capacities)
    non_opt_student = check_for_optimal(students, optimal_student_to_hospital, matching, singles)

    counter = 0  # This is just to not get stuck in loop
    while non_opt_student != "x" and counter < 1000:
        print("Current EMVW:")
        print(matching,singles)
        print(check(matching,hospitals,students))
        print("Current pref:")
        print(hospitals_prefs)
        print(non_opt_student)
        hospitals_prefs, matching, kicked_students = BM(matching, non_opt_student, optimal_student_to_hospital, hospitals_prefs)
        # Nothing to do with kicked students?
        # Improve for hospitals with another EMVW with the submatch from before
        matching, singles = emvw(students, hospitals_prefs, capacities, matching, singles)

        # Did we reach hospital optimality?
        non_opt_student = check_for_optimal(students, optimal_student_to_hospital, matching, singles)
        counter = counter + 1
    if counter >= 1000:
        print("counter==1000")
    print("Final:")
    return matching, singles

# Single step from opt students to opt hospitals. calcualtes opt hospitals anew each time, can be given as input
def single_BM_activation(matching,singles,students,hospitals_prefs,capacities):
    optimal_matching, optimal_singles, optimal_student_to_hospital = reversed_gale_shapley(students, hospitals_prefs,
                                                                                           capacities)
    non_opt_student = check_for_optimal(students, optimal_student_to_hospital, matching, singles)
    if non_opt_student=="x":
        print("This is opt for hospitals already.")
        return matching,singles,hospitals_prefs
    print("Current EMVW:")
    print(matching)
    hospitals_prefs, matching, kicked_students = BM(matching, non_opt_student, optimal_student_to_hospital,
                                                    hospitals_prefs)
    matching, singles = emvw(students, hospitals_prefs, capacities, matching, singles)
    return matching,singles,hospitals_prefs

# Single step from opt students to opt hospitals. recives both non opt student and the stud-hosp dict in advance
def single_BM_activation_premadeS2HANDSTUD(non_opt_student,optimal_student_to_hospital,matching,singles,students,hospitals_prefs,capacities):
    if non_opt_student=="x":
        print("Shouldnt get here")
        return matching,singles,hospitals_prefs
    #print("Current EMVW:")
    #print(matching)
    hospitals_prefs, matching, kicked_students = BM(matching, non_opt_student, optimal_student_to_hospital,
                                                    hospitals_prefs)
    matching, singles = emvw(students, hospitals_prefs, capacities, matching, singles)
    return matching,singles,hospitals_prefs