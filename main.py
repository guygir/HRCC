from HR_Basic import gale_shapley
from HR_Basic0 import gale_shapley0
from Generator import generate_all,generate_all2,generate_all3,generate_all1,generate_all4
from Checker import check
from EMVW import emvw
from Reversed_HR import reversed_gale_shapley
from Divorce import opt_students_to_opt_hospitals, single_BM_activation
from HRCC import lattice_travel,lattice_travel_with_addon
import Counters
import sys, os
import pandas as pd
import xlsxwriter

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Example usage
    students = {
        "R1": ["H1", "H2", "H3", "H4"],
        "R2": ["H1", "H2", "H3", "H4"],
        "R3": ["H3", "H4", "H1", "H2"],
        "R4": ["H3", "H4", "H1", "H2"],
        "R5": ["H2", "H1", "H3", "H4"],
        "R6": ["H2", "H1", "H3", "H4"],
        "R7": ["H4", "H3", "H1", "H2"],
        "R8": ["H4", "H3", "H1", "H2"],
        #"R9": ["H1", "H2", "H3", "H4"],
        #"R10": ["H3", "H4", "H1", "H2"],
    }

    hospitals = {
        "H1": ["R5", "R6", "R1", "R2", "R3", "R4", "R7", "R8"],
        "H2": ["R1", "R2", "R5", "R6", "R3", "R4", "R7", "R8"],
        "H3": ["R7", "R8", "R3", "R4", "R5", "R6", "R1", "R2"],
        "H4": ["R3", "R4", "R7", "R8", "R5", "R6", "R1", "R2"],
    }

    capacities = {
        "H1": 2,
        "H2": 2,
        "H3": 2,
        "H4": 2,
    }

    couples = {
        ("R1", "R2"): [("H2", "H2"), ("H3", "H3"), ("H4", "H4")],
        ("R3", "R4"): [("H3", "H3"), ("H4", "H4")]
    }

    ''' # Run for stats
    for i in range(0,100):
        hospitals, students, capacities = generate_all(20, 20, 0, 0.8, 0.2, 0.5, 1, 1)
        matching,singles = gale_shapley(students, hospitals, capacities) # Singles are unmatched
        matching2 = gale_shapley0(students, hospitals)
        matchingR,singlesR=reversed_gale_shapley(students,hospitals,capacities) # Reversed
        if(matching!=matchingR):
            print(matching, singles)  # This is many to one gale
            print(matchingR, singlesR)  # This is many to one gale reversed
            print(check(matching, hospitals, students), check(matchingR, hospitals, students))
    '''
    # couples= dict of Lists, key=(Stud1,Stud2), value=list of (Hosp1,Hosp2)
    #print(lattice_travel(students, hospitals.copy(), capacities, couples))  # I PUT COPY HERE SO IT WONT CUT THE PREF AT
    # THE END!

    #hospitals, students, capacities = generate_all(25, 10, 1, 1, 1, 1, 2, 2)
    #hospitals, students, capacities,couples = generate_all2(10, 10,1, 1, 1, 1, 10, 20,1,10)
    #print(hospitals,students,capacities,couples)
    #print(lattice_travel(students, hospitals.copy(), capacities, couples))

    #
    # NUMBER OF COUPLES IS BETWEEN 1 TO (INCLUDING) :
    NOC=5
    #
    # NUMBER OF RUNS PER COUPLE IS :
    NOR = 10
    #
    res = [[0 for i in range(4)] for j in range(NOC)] #amount_of_couples,fsa found,fsa_after,bad cases
    for k in range(1,NOC+1):
        for i in range(0,NOR):
            #if i%2==0:
            #    print(i)
            sys.stdout = open(os.devnull, 'w')
            hospitals, students, capacities, couples = generate_all4(30, 5, 1, 1, 1, 1, 5,5, k)
            print(lattice_travel_with_addon(students, hospitals.copy(), capacities, couples))
            sys.stdout = sys.__stdout__
        res[k-1][0]=k
        res[k-1][1]=Counters.fsa_counter
        res[k-1][2]=Counters.same_fsa+Counters.different_fsa
        res[k-1][3]=Counters.bad_case
        Counters.fsa_counter=0
        Counters.bad_case=0
        Counters.same_fsa=0
        Counters.different_fsa=0
        #print(res[k-1])
        #print(Counters.BM)
    # x1,x2,x3=reversed_gale_shapley(students,hospitals,capacities) #matching, single_students, current_hospital
    # print(x1)
    # print(x2)
    # print(x3)
    # print(check(x1,hospitals,students)) # Still true even with bug. so either its a stable matching but not H optimal, or BM has error maybe in logic too
    # Somehow student enters as ravak but he shouldnt be. I wrote why on ipad
    # sub_match = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    # sub_singles = set()
    # print(check(emvw(students,hospitals,capacities,sub_match,sub_singles)[0],hospitals,students))
    # print(emvw(students,hospitals,capacities,sub_match,sub_singles))
    # x1, x2, x3 = reversed_gale_shapley(students, hospitals, capacities)
    # print(check(x1, hospitals, students))
    # print(x1)

    # Issue in BM
    # print(opt_students_to_opt_hospitals(students,hospitals,capacities))
    '''
    sub_match = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    sub_singles = set()
    match, singles = emvw(students, hospitals, capacities, sub_match, sub_singles)  # EMVW using submatch & sub_singles
    print(match)
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}  # COPY!
    match, singles, hospitals_prefs = single_BM_activation(match, singles, students, hospitals_prefs, capacities)
    print(match)
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}  # COPY!
    match, singles, hospitals_prefs = single_BM_activation(match, singles, students, hospitals_prefs, capacities)
    print(match)
    hospitals_prefs = {hospital: list(prefs) for hospital, prefs in hospitals.items()}  # COPY!
    match, singles, hospitals_prefs = single_BM_activation(match, singles, students, hospitals_prefs, capacities)
    print(match)
    '''
    # hospitals, students, capacities = generate_all(10, 10, 0, 0.8, 0.2, 0.5, 1, 1)
    # matching, singles = gale_shapley(students, hospitals, capacities)  # Singles are unmatched
    # matching2 = gale_shapley0(students, hospitals)
    # matchingR, singlesR, student_to_hospital_set = reversed_gale_shapley(students, hospitals, capacities)  # Reversed

    # Prints:
    # print(matching,singles)  # This is many to one gale
    # print(matchingR,singlesR,student_to_hospital_set) # This is many to one gale reversed
    # print(check(matching,hospitals,students),check(matchingR,hospitals,students))
    # print(matching2)  # This is one to one gale
    #
    # sub_match = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    # sub_singles=set()
    # sub_match={"X":list("C"),"Y":list("x"),"Z":list("x")} # Sub match for c
    # print(sub_match)
    #
    # print(emvw(students,hospitals,capacities,sub_match,sub_singles)) # EMVW using submatch & sub_singles
    # print(check(matching,hospitals,students)) # Checking my algo works (^:
    new_list = []
    print("Hospitals Prefs:")  # Prefs:
    list=["Hospital Prefs:"]
    new_list.append(list)
    for hosp in hospitals:
        print(str(hosp) + " : " + str(hospitals[hosp]))
        list=[str(hosp)]
        for x in hospitals[hosp]:
            list.append(x)
        new_list.append(list)
    print("Students Prefs:")
    list = ["Student Prefs:"]
    new_list.append(list)
    for stud in students:
        print(str(stud) + " : " + str(students[stud]))
        list = [str(stud)]
        for x in students[stud]:
            list.append(x)
        new_list.append(list)
    print("Capacities:")
    for cap in capacities:
        print(str(cap) + " : " + str(capacities[cap]))
    print("Couple prefs:")
    list = ["Couples Prefs:"]
    new_list.append(list)
    for couple in couples:
        print(str(couple) + " : " + str(couples[couple]))
        list = [str(couple[0])+","+str(couple[1])]
        for x in couples[couple]:
            list.append(str(x[0])+","+str(x[1]))
        new_list.append(list)
    for i in range(len(res)):
        print(res[i])
    with xlsxwriter.Workbook('test.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(new_list):
            worksheet.write_row(row_num, 0, data)
    #print(Counters.fsa_counter, Counters.same_fsa, Counters.different_fsa,Counters.bad_case)
    # print(x1 != emvw(students, hospitals, capacities, sub_match, sub_singles)[0])
    #
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
