from HR_Basic import gale_shapley
from HR_Basic0 import gale_shapley0
from Generator import generate_all
from Checker import check
from EMVW import emvw
from Reversed_HR import reversed_gale_shapley
from Divorce import opt_students_to_opt_hospitals, single_BM_activation

if __name__ == '__main__':
    print()
    students={}
    hospitals={}
    capacities={}
    with open('Students.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # do something with each line of the text file
            a,b=line.split(":") # a is student
            c=b.rstrip().split(",") # c is list of hospitals.
            students[a]=c
        print("The students' priorities look like this:")
        print(students)
    with open('Hospitals.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # do something with each line of the text file
            a,b=line.split(":") # a is hospital
            c=b.rstrip().split(",") # c is list of students.
            hospitals[a]=c
        print("The hospitals' priorities look like this:")
        print(hospitals)
    with open('Capacities.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # do something with each line of the text file
            a,b=line.split(":") # a is hospital
            c=b.rstrip() # c is the capacity
            capacities[a]=int(c)
        print("The capacities look like this:")
        print(capacities)
    print()
    #
    sub_match = {hospital: list("x" * capacity) for hospital, capacity in capacities.items()}
    sub_singles = set()
    with open('Match.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # do something with each line of the text file
            a,b=line.split(":") # a is hospital
            c=b.rstrip().split(",") # c is list of students.
            if(a=="SINGLE"):
                for i in range(len(c)):
                    sub_singles.add(c[i])
                continue
            for i in range(capacities[a]):
                sub_match[a][i]=c[i]
    print("The given match looks like this:")
    print(sub_match)
    print("And the singles are:")
    print(sub_singles)
    print()
    #
    print("EMVW run would produce the following match:")
    i,j=emvw(students,hospitals,capacities,sub_match,sub_singles)
    print(i)
    print("The single students are:")
    print(j)
    print()
    a,b,c=reversed_gale_shapley(students, hospitals, capacities)
    print("reversed gale shapley run would produce the following match:")
    print(a)
    print("The single students are:")
    print(b)
    print("The dict that shows for each student his hospital is:")
    print(c)
