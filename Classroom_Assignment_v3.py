'''
Idea:
=====

If C1.professor == C2.professor:
    C1.time != C2.time
    C1.room == C2.room
    C1.students == C2.students

If C1.room == C2.room:
    C1.time != C2.time
    C1.professor == C2.professor
    C1.students == C2.students

If C1.time == C2.time:
    C1.room != C2.room
    C1.professor != C2.professor
    C1.students != C2.students

If C1.students == C2.students:
    C1.time != C2.time
    C1.room == C2.room
    C1.professor == C2.professor
'''

'''
CONFLICT TYPES:
    1 = Same Professor
    2 = Same Room Number
    3 = Same Time Slot
    4 = Same Students
'''
#     working_schedule = {"Courses": [], "Time and Room": {}, "Conflicts and Conflict Types": {}}
def Update_Working_Schedule(course_num, working_schedule, course_conflicts, conflict_types):
    if course_num in working_schedule["Courses"]:
        for i in range(len(course_conflicts)):
            working_schedule["Conflicts and Conflict Types"][course_num][course_conflicts[i]].update(conflict_types[i])

    else:
        working_schedule["Courses"].append(course_num)
        working_schedule["Time and Room"][course_num] = [1, 100]
        working_schedule["Conflicts and Conflict Types"][course_num] = {}
        for i in range(len(course_conflicts)):
            working_schedule["Conflicts and Conflict Types"][course_num][course_conflicts[i]] = {}
        for i in range(len(course_conflicts)):
            working_schedule["Conflicts and Conflict Types"][course_num][course_conflicts[i]] = conflict_types[i]


    for course in course_conflicts:
        if course in working_schedule:
            working_schedule["Conflicts and Conflict Types"][course][course_conflicts[0]].update(conflict_types[0])
        
        else:
            working_schedule["Courses"].append(course)
            working_schedule["Time and Room"][course] = [1, 100]
            working_schedule["Conflicts and Conflict Types"][course] = {course_num: conflict_types[course_conflicts.index(course)]}

    print(working_schedule)



def Add_Course(course_num, all_conflict_types, working_schedule):
    course_conflicts = []
    conflict_types = []

    counter = 0

    while True:
        counter += 1

        print('\n=========================================')
        print('If there are no conflicts, enter "None"')
        print('=========================================', end='')

        # =========================
        # GETTING COURSE CONFLICTS
        # =========================
        if counter == 1:
            course_conflict_input = input(f'\nWhat course does C{course_num} conflict with? (If none, enter "None"): ').strip().lower()
            if course_conflict_input == "none" or course_conflict_input == "done": break
            while True:
                if not course_conflict_input.isdigit():
                    print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"Please enter a digit for the Course in Conflict")
                    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                    course_conflict_input = input(f'What course does C{course_num} conflict with? (If none, enter "None"): ').strip().lower()
                    continue
                elif course_conflict_input == course_num:
                    print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"Course cannot conflict with itself")
                    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                    course_conflict_input = input(f'What course does C{course_num} conflict with? (If none, enter "None"): ').strip().lower()
                    continue
                break

            
            if course_conflict_input == "none": break

            course_conflicts.append(course_conflict_input)

        else:
            print('\n=========================================')
            print('If done with your selection, enter "Done"')
            print('=========================================', end='')

            course_conflict_input = input(f'\nWhat course does C{course_num} conflict with?: ').strip().lower()
            while not course_conflict_input.isdigit():
                if course_conflict_input == "done": break
                print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Course C{course_conflict_input} does not exist")
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!\n")
                course_conflict_input = input(f'What course does C{course_num} conflict with?: ').strip().lower()
            
            if course_conflict_input == "done": break

            course_conflicts.append(course_conflict_input)

        # if course_conflict_input in working_schedule:
        #     working_schedule[course_conflict_input]["Conflicts"].append(course_num)
        
        # else:
        #     working_schedule[course_conflict_input] = {"Course Number": course_conflict_input, "Room Number": 100, "Time Slot": 0, "Conflicts": [course_num], "Conflict Types": []}

        # ======================
        # GETTING CONFLICT TYPES
        # ======================
        print("TYPES OF CONFLICT:\n",
            "\t1. Courses have the Same Professor\n"
            "\t2. Courses have the Same Room Number\n"
            "\t3. Courses have the Same Time Slot\n"
            "\t4. Courses have the Same Students"
        )
        conflict_type_input = input(f"\nWhich type of conflict do these courses have (1-4)?: ").strip().lower()
        while conflict_type_input not in all_conflict_types:
            if conflict_type_input == "done":
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("You must enter a conflict type before finishing")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            else:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("That is not a Conflict Type")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
            conflict_type_input = input(f"Which type of conflict do these courses have (1-4)?: ").strip().lower()

        conflict_types.append(conflict_type_input)

    Update_Working_Schedule(course_num, working_schedule, course_conflicts, conflict_types)

    return working_schedule


#     working_schedule = {"Courses": [], "Time and Room": {}, "Conflicts and Conflict Types": {}}
def Schedule_Courses(working_schedule, num_time_slots, num_rooms):
    conflicts_present = True
    

    while conflicts_present:
        conflicts_present = False

        for course_1 in working_schedule["Courses"]:
            for course_2 in working_schedule["Courses"]:
                if course_1 != course_2:
                    if working_schedule["Time and Room"][course_1] == working_schedule["Time and Room"][course_2]:
                        conflicts_present = True
                        working_schedule["Time and Room"][course_2][1] += 1

                        if working_schedule["Time and Room"][course_2][1] >= (100 + (num_rooms)):
                            working_schedule["Time and Room"][course_2][1] = 100
                            working_schedule["Time and Room"][course_2][0] += 1
                            if working_schedule["Time and Room"][course_2][0] > num_time_slots:
                                working_schedule["Time and Room"][course_2][0] = 1



            for conflicted_course in working_schedule["Conflicts and Conflict Types"][course_1]:
                conflict_type = working_schedule["Conflicts and Conflict Types"][course_1][conflicted_course]

                # Time Slot needs to change
                if conflict_type in ["1", "2", "4"]:
                    if working_schedule["Time and Room"][course_1][0] == working_schedule["Time and Room"][conflicted_course][0]:
                        conflicts_present = True
                        working_schedule["Time and Room"][conflicted_course][0] += 1

                        if working_schedule["Time and Room"][conflicted_course][0] > num_time_slots:
                            working_schedule["Time and Room"][conflicted_course][0] = 1
                            working_schedule["Time and Room"][conflicted_course][1] += 1
                            if working_schedule["Time and Room"][conflicted_course][1] >= (100 + (num_rooms)):
                                working_schedule["Time and Room"][conflicted_course][1] = 100

                # Room Number needs to change
                elif conflict_type == "3":
                    if working_schedule["Time and Room"][course_1][1] == working_schedule["Time and Room"][conflicted_course][1] and working_schedule["Time and Room"][course_1][0] == working_schedule["Time and Room"][conflicted_course][0]:
                        conflicts_present = True
                        working_schedule["Time and Room"][conflicted_course][1] += 1

                        if working_schedule["Time and Room"][conflicted_course][1] >= (100 + (num_rooms)):
                            working_schedule["Time and Room"][conflicted_course][1] = 100
                            working_schedule["Time and Room"][conflicted_course][0] += 1
                            if working_schedule["Time and Room"][conflicted_course][0] > num_time_slots:
                                working_schedule["Time and Room"][conflicted_course][0] = 1
                
                else:
                    print("!!! ERROR OCCURRED !!!")
                                

    Print_Current_Schedule(working_schedule)
    return working_schedule


def Print_Current_Schedule(schedule):
    """
    working_schedule = {"Courses": [], "Time and Room": {}, "Conflicts and Conflict Types": {}}
    """
    # print(schedule)
    for course in schedule["Courses"]:
        print(f"Course: C{course} | Time Slot: {schedule['Time and Room'][course][0]} | Room: {schedule['Time and Room'][course][1]}")


def main():
    '''
    Same Professor:
        C1 <-> C2 (P=0)     (T!=)
        C5 <-> C6 (P=1)     (T!=)

    Same Room Number:
        C1 <-> C3 (R=100)   (T!=)

    Same Time Slot:
        C2 <-> C4 (T=0)     (P,R,S!=)
        C4 <-> C6 (T=1)     (P,R,S!=)

    Same Students:
        C3 <-> C5 (S=0)     (T!=)
    '''

    '''
    CONFLICT TYPES:
        1 = Same Professor
        2 = Same Room Number
        3 = Same Time Slot
        4 = Same Students
    '''
    all_conflict_types = [
        '1',    # Same Professor
        '2',    # Same Room
        '3',    # Same Time Slot
        '4'     # Same Students
    ]

    # The dictionary we will use to construct our schedule
    working_schedule = {"Courses": [], "Time and Room": {}, "Conflicts and Conflict Types": {}}

    num_time_slots = int(input("How many time slots are available? "))
    num_rooms = int(input("How many rooms are available? "))

    # Getting the course number
    course_num = input("\nEnter a Course Number: ")
    while course_num != "-1":
        while not(course_num.isdigit()):
            course_num = input("Please enter a digit for the Course Number: ")

        
        working_schedule = Add_Course(course_num, all_conflict_types, working_schedule)
        working_schedule = Schedule_Courses(working_schedule, num_time_slots, num_rooms)

        course_num = input("\nEnter a Course Number: ")


if __name__ == "__main__":
    DEBUG_MODE = False

    # working_schedule = {'Courses': ['1', '2', '3'], 'Time and Room': {'1': [1, 100], '2': [1, 100], '3': [1, 100]}, 'Conflicts and Conflict Types': {'1': {'2': '4', '3': '23'}, '2': {'1': '4'}, '3': {'1': '3'}}}
    # working_schedule = {'Courses': ['1', '2', '3'], 'Time and Room': {'1': [1, 100], '2': [1, 100], '3': [1, 100]}, 'Conflicts and Conflict Types': {'1': {'2': '4', '3': '1'}, '2': {'1': '4'}, '3': {'1': '1'}}}
    working_schedule = {
    'Courses': ['1', '2', '3', '4'], 
    'Time and Room': {'1': [1, 100], '2': [1, 100], '3': [1, 100], '4': [1, 100]}, 
    'Conflicts and Conflict Types': {
        '1': {'2': '1'}, 
        '2': {'1': '1', '3': '4'}, 
        '3': {'2': '4', '4': '3'},
        '4': {'3': '3'}
    }
}
    num_time_slots = 4
    num_rooms = 3

    if DEBUG_MODE:
        Schedule_Courses(working_schedule, num_time_slots, num_rooms)

    else:
        main()