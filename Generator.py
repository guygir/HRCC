import numpy as np
import random

def generate_all(num_of_students, num_of_hospitals, p_low_hospital, p_high_hospital, p_low_student, p_high_student
                 , low_capacity, high_capacity):
    hospitals = {}
    students = {}
    capacities={}
    for i in range(num_of_hospitals):
        lst=["Student " + str(x) for x in range(0, num_of_students) if
                                           np.random.uniform(0, 1) <= np.random.uniform(p_low_student, p_high_student)]
        random.shuffle(lst)
        hospitals["Hospital " + str(i)] = lst

    for i in range(num_of_hospitals):
        capacities["Hospital " + str(i)] = np.random.randint(low_capacity, high_capacity+1)

    for i in range(num_of_students):
        lst=["Hospital " + str(x) for x in range(0, num_of_hospitals) if
                                         np.random.uniform(0, 1) <= np.random.uniform(p_low_hospital, p_high_hospital)]
        random.shuffle(lst)
        students["Student " + str(i)] = lst

    return hospitals,students,capacities

def generate_all1(num_of_students, num_of_hospitals, p_low_hospital, p_high_hospital, p_low_student, p_high_student
                 , low_capacity, high_capacity,num_of_couples): #same hopsital, method 1
    hospitals = {}
    students = {}
    capacities={}
    couples={}
    for i in range(num_of_hospitals):
        lst=["Student " + str(x) for x in range(0, num_of_students) if
                                           np.random.uniform(0, 1) <= np.random.uniform(p_low_student, p_high_student)]
        random.shuffle(lst)
        hospitals["Hospital " + str(i)] = lst

    for i in range(num_of_hospitals):
        capacities["Hospital " + str(i)] = np.random.randint(low_capacity, high_capacity+1)

    for i in range(num_of_students):
        lst=["Hospital " + str(x) for x in range(0, num_of_hospitals) if
                                         np.random.uniform(0, 1) <= np.random.uniform(p_low_hospital, p_high_hospital)]
        random.shuffle(lst)
        students["Student " + str(i)] = lst

    for i in range(num_of_couples):
        cnt=0
        st1="Student " + str(2*i)
        st2="Student " + str((2*i)+1)
        st2_limit=-1
        lst=[]
        while(cnt<len(students[st1])):
            curr_hosp_1=students[st1][cnt]
            if(curr_hosp_1 not in students[st2]):
                cnt=cnt+1
                continue
            if(students[st2].index(curr_hosp_1)<st2_limit):
                cnt=cnt+1
                continue
            st2_limit=students[st2].index(curr_hosp_1)
            lst.append((curr_hosp_1,curr_hosp_1))
            cnt=cnt+1

        couples[("Student "+str(2*i),"Student "+str((2*i)+1))]=lst

    return hospitals,students,capacities,couples


def generate_all2(num_of_students, num_of_hospitals, p_low_hospital, p_high_hospital, p_low_student, p_high_student
                 , low_capacity, high_capacity,num_of_couples,num_of_hosps_per_couple): #consistent randoms
    hospitals = {}
    students = {}
    capacities={}
    couples={}
    for i in range(num_of_hospitals):
        lst=["Student " + str(x) for x in range(0, num_of_students) if
                                           np.random.uniform(0, 1) <= np.random.uniform(p_low_student, p_high_student)]
        random.shuffle(lst)
        hospitals["Hospital " + str(i)] = lst

    for i in range(num_of_hospitals):
        capacities["Hospital " + str(i)] = np.random.randint(low_capacity, high_capacity+1)

    for i in range(num_of_students):
        lst=["Hospital " + str(x) for x in range(0, num_of_hospitals) if
                                         np.random.uniform(0, 1) <= np.random.uniform(p_low_hospital, p_high_hospital)]
        random.shuffle(lst)
        students["Student " + str(i)] = lst

    for i in range(num_of_couples):
        cnt=0
        approved=0
        st1="Student " + str(2*i)
        st2="Student " + str((2*i)+1)
        st2_limit=-1
        st1_limit=-1
        occ_1=[]
        occ_2=[]
        lst=[]
        while(approved<num_of_hosps_per_couple and cnt<len(students[st1])):
            ind1=np.random.randint(0,len(students[st1]))
            ind2=np.random.randint(0, len(students[st2]))
            curr_hosp_1=students[st1][ind1]
            curr_hosp_2 = students[st2][ind2]
            if(ind1 in occ_1 or ind2 in occ_2):
                cnt=cnt+1
                continue
            if(curr_hosp_1 not in students[st1] or curr_hosp_2 not in students[st2]):
                cnt=cnt+1
                continue
            if(students[st1].index(curr_hosp_1)<st1_limit or students[st2].index(curr_hosp_2)<st2_limit):
                cnt=cnt+1
                continue
            st2_limit=students[st2].index(curr_hosp_2)
            st1_limit = students[st1].index(curr_hosp_1)
            occ_1.append(ind1)
            occ_2.append(ind2)
            lst.append((curr_hosp_1,curr_hosp_2))
            approved=approved+1
            cnt=cnt+1

        couples[("Student "+str(2*i),"Student "+str((2*i)+1))]=lst

    return hospitals,students,capacities,couples

def generate_all3(num_of_students, num_of_hospitals, p_low_hospital, p_high_hospital, p_low_student, p_high_student
                 , low_capacity, high_capacity,num_of_couples): # Nitsan Method
    hospitals = {}
    students = {}
    capacities={}
    couples={}
    for i in range(num_of_hospitals):
        lst=["Student " + str(x) for x in range(0, num_of_students) if
                                           np.random.uniform(0, 1) <= np.random.uniform(p_low_student, p_high_student)]
        random.shuffle(lst)
        hospitals["Hospital " + str(i)] = lst

    for i in range(num_of_hospitals):
        capacities["Hospital " + str(i)] = np.random.randint(low_capacity, high_capacity+1)

    for i in range(num_of_students):
        lst=["Hospital " + str(x) for x in range(0, num_of_hospitals) if
                                         np.random.uniform(0, 1) <= np.random.uniform(p_low_hospital, p_high_hospital)]
        random.shuffle(lst)
        students["Student " + str(i)] = lst

    for i in range(num_of_couples):
        st1="Student " + str(2*i)
        st2="Student " + str((2*i)+1)
        len1=len(students[st1])
        len2 = len(students[st2])
        final_len=min(len1,len2)
        lst=[]
        for j in range(final_len-1):
            lst.append((students[st1][j], students[st2][j]))
            lst.append((students[st1][j], students[st2][j+1]))

        couples[("Student "+str(2*i),"Student "+str((2*i)+1))]=lst

    return hospitals,students,capacities,couples

def generate_all4(num_of_students, num_of_hospitals, p_low_hospital, p_high_hospital, p_low_student, p_high_student
                 , low_capacity, high_capacity,num_of_couples): # Nitsan2 Method
    hospitals = {}
    students = {}
    capacities={}
    couples={}
    for i in range(num_of_hospitals):
        lst=["Student " + str(x) for x in range(0, num_of_students) if
                                           np.random.uniform(0, 1) <= np.random.uniform(p_low_student, p_high_student)]
        random.shuffle(lst)
        hospitals["Hospital " + str(i)] = lst

    for i in range(num_of_hospitals):
        capacities["Hospital " + str(i)] = np.random.randint(low_capacity, high_capacity+1)

    for i in range(num_of_students):
        lst=["Hospital " + str(x) for x in range(0, num_of_hospitals) if
                                         np.random.uniform(0, 1) <= np.random.uniform(p_low_hospital, p_high_hospital)]
        random.shuffle(lst)
        students["Student " + str(i)] = lst

    for i in range(num_of_couples):
        st1="Student " + str(2*i)
        st2="Student " + str((2*i)+1)
        len1=len(students[st1])
        students[st2]=students[st1]
        lst=[]
        for j in range(len1-1):
            lst.append((students[st1][j], students[st1][j]))
        couples[("Student "+str(2*i),"Student "+str((2*i)+1))]=lst

    return hospitals,students,capacities,couples
