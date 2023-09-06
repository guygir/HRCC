import math
import random
import Counters
from HR_Basic import gale_shapley
from HR_Basic0 import gale_shapley0
from Generator import generate_all
from Checker import check
from EMVW import emvw
from Reversed_HR import reversed_gale_shapley
from Divorce import opt_students_to_opt_hospitals, single_BM_activation, single_BM_activation_premadeS2HANDSTUD


# couples= dict of Lists, key=(Stud1,Stud2), value=list of (Hosp1,Hosp2)


# I assume the stability of the match is given by emvw. So only need to check feasibility
# If FSA returns None,None, otherwise returns a pair c1,c2 that breaks FSA.
# I CUT PREFS HERE! IMPORTANT!
def FSA(current_match, current_singles, couples):
    for couple in couples:
        # print("debg:",current_match)
        current_couple_legit = False
        c1, c2 = couple
        # print("debg:", c1,c2)
        if c1 in current_singles and c2 in current_singles:  # If both unmatched
            continue
        # Now need to check if theyre both matched in one of their couple prefs.
        c1_hosp = None
        for hosp in current_match:
            if c1 in current_match[hosp]:
                c1_hosp = hosp  # c1_hosp is the hospital of c1 in the couple
                break
        for hosp_couple in couples[couple]:
            h1, h2 = hosp_couple
            if h1 == c1_hosp:  # For each pref of the couple with c1_hosp check if c2 fits the pref
                if c2 in current_match[h2]:
                    current_couple_legit = True
                    break
        if current_couple_legit == False:  # This couple breaks FSA
            print(str(c1) + "," + str(c2) + ", arent satisfied with their couple's prefs.")
            return c1, c2
    # If we got here no couple broke FSA
    return None, None


# Returns hosp1,hosp2 for c1,c2 in couple
def next(current_match, couples, couple, students):
    c1, c2 = couple
    c1_hosp = None
    c2_hosp = None
    counter = 0
    for hospital in current_match:
        if c1 in current_match[hospital]:
            c1_hosp = hospital
            counter = counter + 1
        if c2 in current_match[hospital]:
            c2_hosp = hospital
            counter = counter + 1
        if counter == 2:
            break
    current_hosp_couple = (c1_hosp, c2_hosp)
    # Case 1
    for hosp_couple in couples[couple]:
        if hosp_couple == current_hosp_couple:
            return c1_hosp, c2_hosp
    # Case 2
    couple_prefs = couples[couple]
    first_pref = couple_prefs[0]
    c1_pref_hosp, c2_pref_hosp = first_pref
    c1_prefs = students[c1]
    c2_prefs = students[c2]
    c1_hosp_index = c1_prefs.index(c1_hosp)
    c2_hosp_index = c2_prefs.index(c2_hosp)
    c1_pref_hosp_index = c1_prefs.index(c1_pref_hosp)
    c2_pref_hosp_index = c2_prefs.index(c2_pref_hosp)
    if c1_pref_hosp_index < c1_hosp_index or c2_pref_hosp_index < c2_hosp_index:
        return None, None  # First pref doesn't stand the needed equality so so do the rest
    for i in range(1, len(couple_prefs)):
        pref = couple_prefs[i]
        c1_pref_hosp, c2_pref_hosp = pref
        c1_pref_hosp_index = c1_prefs.index(c1_pref_hosp)
        c2_pref_hosp_index = c2_prefs.index(c2_pref_hosp)
        if c1_pref_hosp_index < c1_hosp_index or c2_pref_hosp_index < c2_hosp_index:
            chosen_hosp_couple = couple_prefs[i - 1]  # Return the last valid one
            chosen_h1, chosen_h2 = chosen_hosp_couple
            return chosen_h1, chosen_h2

    # If got here, ALL of the prefs maintain the condition, so return the last
    chosen_hosp_couple = couple_prefs[len(couple_prefs) - 1]
    chosen_h1, chosen_h2 = chosen_hosp_couple
    return chosen_h1, chosen_h2


# HRCC
# Last 2 arguments are optional and are for us to enter a current match instead of startign from EMVW.
# CHECK THIS! ^
def lattice_travel(students, hospitals, capacities, couples, given_match=None, given_singles=None):
    # A STAGE - prep
    sub_match = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    sub_singles = set()
    if given_match is None:
        students_optimal_match, students_optimal_singles = emvw(students, hospitals, capacities, sub_match, sub_singles)
    else:
        students_optimal_match = given_match
        students_optimal_singles = given_singles
    hospitals_optimal_match, hospitals_optimal_singles, hospitals_optimal_studToHospDict = reversed_gale_shapley(
        students, hospitals, capacities)
    # print(students_optimal_match,hospitals_optimal_match)

    # B STAGE - if there is a couple when only 1 is matched
    mod = 0
    for couple in couples:
        c1, c2 = couple
        if c1 not in students_optimal_singles:
            mod = mod + 1
        if c2 not in students_optimal_singles:
            mod = mod + 1
        if mod % 2 == 1:
            print("Out of the two students:" + str(c1) + "," + str(
                c2) + ", one of them if single in the optimal students' matching and one of them isn't. So, there's no FSA.")
            return False,False

    # C STAGE - checking if given emvw is FSA
    current_match = students_optimal_match
    current_singles = students_optimal_singles
    print("This is 2nd run:")
    print(current_match)
    print(current_singles)
    print(students)
    print(hospitals)
    couple = FSA(current_match, current_singles, couples)
    c1, c2 = couple
    if c1 == None:  # No couple broke FSA
        print("FSA found!")
        return current_match, current_singles
    # If we got here, c1,c2 broke feasibility.
    # D STAGE - handle the couple(s) that break feasiblity
    fsa_found_counter = 0
    while fsa_found_counter < 10000:
        print("Current match at: "+str(fsa_found_counter))
        print(current_match)
        # print(fsa_found_counter)
        fsa_found_counter = fsa_found_counter + 1
        next_h1, next_h2 = next(current_match, couples, couple, students)
        # Case A
        if next_h1 == None:
            print("Next func return None so there's no FSA")
            return False,False
        # Case B
        reversed_hosp_c1 = hospitals_optimal_studToHospDict[c1]
        reversed_hosp_c2 = hospitals_optimal_studToHospDict[c2]
        if(current_match!=hospitals_optimal_match):
            print("OPT FOR EACH SIDE IS DIFFERENT!")
        # print(c1,reversed_hosp_c1,current_match,hospitals_optimal_match)
        if c1 not in current_match[reversed_hosp_c1]:
            # BM on c1
            Counters.BM=Counters.BM+1
            current_match, current_singles, hospitals = single_BM_activation_premadeS2HANDSTUD(c1,
                                                                                               hospitals_optimal_studToHospDict,
                                                                                               current_match,
                                                                                               current_singles,
                                                                                               students, hospitals,
                                                                                               capacities)
            couple = FSA(current_match, current_singles, couples)
            c1, c2 = couple
            if c1 == None:  # No couple broke FSA
                print("FSA found!")
                return current_match, current_singles
            # Not FSA, so we need another round
            continue
        if c2 not in current_match[reversed_hosp_c2]:
            # BM on c2
            Counters.BM = Counters.BM + 1
            current_match, current_singles, hospitals = single_BM_activation_premadeS2HANDSTUD(c2,
                                                                                               hospitals_optimal_studToHospDict,
                                                                                               current_match,
                                                                                               current_singles,
                                                                                               students, hospitals,
                                                                                               capacities)
            couple = FSA(current_match, current_singles, couples)
            c1, c2 = couple
            if c1 == None:  # No couple broke FSA
                print("FSA found!")
                return current_match, current_singles
            # Not FSA, so we need another round
            continue
        # If we got here, both are at their worst, so no FSA
        print("Both students are at their least optimal choice, so no FSA available, counter:" + str(fsa_found_counter))
        return False,False
    # If we got here, counter exceeded
    print("Counter exceeded 10,000, something went wrong or youre using a huge database")
    return None,None


def lattice_travel_with_addon(students, hospitals, capacities, couples, given_match=None, given_singles=None):
    # A STAGE - prep
    sub_match = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    sub_singles = set()
    if given_match is None:
        students_optimal_match, students_optimal_singles = emvw(students, hospitals, capacities, sub_match, sub_singles)
    else:
        students_optimal_match = given_match
        students_optimal_singles = given_singles
    hospitals_optimal_match, hospitals_optimal_singles, hospitals_optimal_studToHospDict = reversed_gale_shapley(
        students, hospitals, capacities)
    # print(students_optimal_match,hospitals_optimal_match)

    # B STAGE - if there is a couple when only 1 is matched
    mod = 0
    for couple in couples:
        c1, c2 = couple
        if c1 not in students_optimal_singles:
            mod = mod + 1
        if c2 not in students_optimal_singles:
            mod = mod + 1
        if mod % 2 == 1:
            print("Out of the two students:" + str(c1) + "," + str(
                c2) + ", one of them if single in the optimal students' matching and one of them isn't. So, there's no FSA.")
            return False

    # C STAGE - checking if given emvw is FSA
    current_match = students_optimal_match
    current_singles = students_optimal_singles
    couple = FSA(current_match, current_singles, couples)
    c1, c2 = couple
    if c1 == None:  # No couple broke FSA
        print("FSA found!")
        Counters.fsa_counter=Counters.fsa_counter+1

        first_match=current_match
        first_singles=current_singles
        students["Student -1"]=["Hospital " + str(x) for x in range(0, len(hospitals))] # new stud
        for hosp in hospitals: # put him in random place in his hospital
            rand_index=random.randint(0,len(hospitals[hosp]))
            hospitals[hosp]=hospitals[hosp][:rand_index]+["Student -1"]+hospitals[hosp][rand_index:]
        # Lets see if stuff changed. I give here the prev match!
        second_match,second_singles=lattice_travel(students,hospitals,capacities,couples)
        if (second_match == False):
            print("No FSA at the 2nd time")
            return None, None
        if(second_match==first_match):
            print("Matches are the same!")
            Counters.same_fsa = Counters.same_fsa+1
        else:
            print("Matches are different! Lets compare:")
            Counters.different_fsa = Counters.different_fsa + 1
            #print(first_match,first_singles)
            #print(second_match,second_singles)
            compare={}
            for stud in students:
                compare[stud]=[len(hospitals)+0.5,len(hospitals)+0.5] #INF
            for hosp in hospitals:
                hosp_list1=first_match[hosp]
                for stud in hosp_list1: # NEEDS TO BE DIFF THAN X!
                    if stud!="x":
                        compare[stud][0]=students[stud].index(hosp)
                hosp_list2= second_match[hosp]
                for stud in hosp_list2: # NEEDS TO BE FIDD THAN X!
                    if stud != "x":
                        compare[stud][1] = students[stud].index(hosp)
            #print(compare)
            for stud in compare:
                if compare[stud][0]>compare[stud][1] and stud!="Student -1":
                    print(str(stud)+" Has improved his situation - that doesn't make sense...")
                    Counters.bad_case=Counters.bad_case+1
                    exit()



            print("END!")

        # no need to return
        return current_match, current_singles
    # If we got here, c1,c2 broke feasibility.
    # D STAGE - handle the couple(s) that break feasiblity
    fsa_found_counter = 0
    while fsa_found_counter < 10000:
        print("Current match at: "+str(fsa_found_counter))
        print(current_match)
        # print(fsa_found_counter)
        fsa_found_counter = fsa_found_counter + 1
        next_h1, next_h2 = next(current_match, couples, couple, students)
        # Case A
        if next_h1 == None:
            print("Next func return None so there's no FSA")
            return False
        # Case B
        reversed_hosp_c1 = hospitals_optimal_studToHospDict[c1]
        reversed_hosp_c2 = hospitals_optimal_studToHospDict[c2]
        if(current_match!=hospitals_optimal_match):
            print("OPT FOR EACH SIDE IS DIFFERENT!")
        # print(c1,reversed_hosp_c1,current_match,hospitals_optimal_match)
        if c1 not in current_match[reversed_hosp_c1]:
            # BM on c1
            current_match, current_singles, hospitals = single_BM_activation_premadeS2HANDSTUD(c1,
                                                                                               hospitals_optimal_studToHospDict,
                                                                                               current_match,
                                                                                               current_singles,
                                                                                               students, hospitals,
                                                                                               capacities)
            couple = FSA(current_match, current_singles, couples)
            c1, c2 = couple
            if c1 == None:  # No couple broke FSA
                print("FSA found!")
                Counters.fsa_counter = Counters.fsa_counter+1
                first_match = current_match
                first_singles = current_singles
                students["Student -1"] = ["Hospital " + str(x) for x in range(0, len(hospitals))]  # new stud
                for hosp in hospitals:  # put him in random place in his hospital
                    rand_index = random.randint(0, len(hospitals[hosp]))
                    hospitals[hosp] = hospitals[hosp][:rand_index] + ["Student -1"] + hospitals[hosp][rand_index:]
                # Lets see if stuff changed. I give here the prev match!
                second_match, second_singles = lattice_travel(students, hospitals, capacities, couples)
                if(second_match==False):
                    print("No FSA at the 2nd time")
                    return None,None
                if (second_match == first_match):
                    print("Matches are the same!")
                    Counters.same_fsa = Counters.same_fsa + 1
                else:
                    print("Matches are different! Lets compare:")
                    Counters.different_fsa = Counters.different_fsa + 1
                    print(first_match, first_singles)
                    print(second_match, second_singles)
                    compare = {}
                    for stud in students:
                        compare[stud] = [len(hospitals) + 0.5, len(hospitals) + 0.5]  # INF
                    for hosp in hospitals:
                        hosp_list1 = first_match[hosp]
                        for stud in hosp_list1:
                            if stud != "x":
                                compare[stud][0] = students[stud].index(hosp)
                        hosp_list2 = second_match[hosp]
                        for stud in hosp_list2:
                            if stud != "x":
                                compare[stud][1] = students[stud].index(hosp)
                    print(compare)
                    for stud in compare:
                        if compare[stud][0] > compare[stud][1] and stud != "Student -1":
                            print(str(stud) + " Has improved his situation - that doesn't make sense...")
                            Counters.bad_case = Counters.bad_case + 1

                    print("END!")

                # no need to return
                return current_match, current_singles
            # Not FSA, so we need another round
            continue
        if c2 not in current_match[reversed_hosp_c2]:
            # BM on c2
            current_match, current_singles, hospitals = single_BM_activation_premadeS2HANDSTUD(c2,
                                                                                               hospitals_optimal_studToHospDict,
                                                                                               current_match,
                                                                                               current_singles,
                                                                                               students, hospitals,
                                                                                               capacities)
            couple = FSA(current_match, current_singles, couples)
            c1, c2 = couple
            if c1 == None:  # No couple broke FSA
                print("FSA found!")
                Counters.fsa_counter = Counters.fsa_counter + 1
                first_match = current_match
                first_singles = current_singles
                students["Student -1"] = ["Hospital " + str(x) for x in range(0, len(hospitals))]  # new stud
                for hosp in hospitals:  # put him in random place in his hospital
                    rand_index = random.randint(0, len(hospitals[hosp]))
                    hospitals[hosp] = hospitals[hosp][:rand_index] + ["Student -1"] + hospitals[hosp][rand_index:]
                # Lets see if stuff changed. I give here the prev match!
                second_match, second_singles = lattice_travel(students, hospitals, capacities, couples)
                if (second_match == False):
                    print("No FSA at the 2nd time")
                    return None, None
                if (second_match == first_match):
                    print("Matches are the same!")
                    Counters.same_fsa = Counters.same_fsa + 1
                else:
                    print("Matches are different! Lets compare:")
                    Counters.different_fsa = Counters.different_fsa + 1
                    print(first_match, first_singles)
                    print(second_match, second_singles)
                    compare = {}
                    for stud in students:
                        compare[stud] = [len(hospitals) + 0.5, len(hospitals) + 0.5]  # INF
                    for hosp in hospitals:
                        hosp_list1 = first_match[hosp]
                        for stud in hosp_list1:
                            if stud != "x":
                                compare[stud][0] = students[stud].index(hosp)
                        hosp_list2 = second_match[hosp]
                        for stud in hosp_list2:
                            if stud != "x":
                                compare[stud][1] = students[stud].index(hosp)
                    for stud in compare:
                        if compare[stud][0] > compare[stud][1] and stud != "Student -1":
                            print(str(stud) + " Has improved his situation - that doesn't make sense...")
                            Counters.bad_case = Counters.bad_case + 1

                    print("END!")

                # no need to return
                return current_match, current_singles
            # Not FSA, so we need another round
            continue
        # If we got here, both are at their worst, so no FSA
        print("Both students are at their least optimal choice, so no FSA available, counter:" + str(fsa_found_counter))
        return False
    # If we got here, counter exceeded
    print("Counter exceeded 10,000, something went wrong or youre using a huge database")
    return None


