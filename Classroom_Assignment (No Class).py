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
def add_course(course_num, all_conflict_types):
    course_conflicts = []
    conflict_types = []

    counter = 0

    while True:
        counter += 1

        print('=========================================')
        print('If done with your selection, enter "Done"')
        print('=========================================')

        # =========================
        # GETTING COURSE CONFLICTS
        # =========================
        if counter == 1:
            course_conflict_input = input(f'\nWhat course does C{course_num} conflict with? (If none, enter "None"): ').strip().lower()
            if course_conflict_input == "none" or course_conflict_input == "done": break
            while not course_conflict_input.isdigit():
                print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Please enter a digit for the Course in Conflict")
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
                course_conflict_input = input(f'What course does C{course_num} conflict with? (If none, enter "None"): ').strip().lower()
            
            if course_conflict_input == "none": break

            course_conflicts.append(course_conflict_input)

        else:
            course_conflict_input = input(f'\nWhat course does C{course_num} conflict with?: ').strip().lower()
            while not course_conflict_input.isdigit():
                if course_conflict_input == "done": break
                print(f"\n!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"Course C{course_conflict_input} does not exist")
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!\n")
                course_conflict_input = input(f'What course does C{course_num} conflict with?: ').strip().lower()
            
            if course_conflict_input == "done": break

            course_conflicts.append(course_conflict_input)

        if course_conflict_input in working_schedule:
            working_schedule[course_conflict_input]["Conflicts"].append(course_num)
        
        else:
            working_schedule[course_conflict_input] = {"Course Number": course_conflict_input, "Room Number": 100, "Time Slot": 0, "Conflicts": [course_num], "Conflict Types": []}

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

        working_schedule[course_conflict_input]["Conflict Types"].append(conflict_type_input)



    return course_conflicts, conflict_types


def schedule_courses(working_schedule, course_to_add):
    course_number = course_to_add["Course Number"]
    if len(working_schedule) != 0:
        room_number = course_to_add["Room Number"]
        time_slot = course_to_add["Time Slot"]
        conflicts = course_to_add["Conflicts"]

        for course in working_schedule:
            if (working_schedule[course]["Course Number"] in conflicts) or (course_number in working_schedule[course]["Conflicts"]):
                for conflict_type in conflict_types:
                    if conflict_type == "1":
                        course_to_add["Time Slot"] += 1
                    elif conflict_type == "2":
                        course_to_add["Time Slot"] += 1
                    elif conflict_type == "3":
                        course_to_add["Room Number"] += 1
                    elif conflict_type == "4":
                        course_to_add["Time Slot"] += 1

        working_schedule[course_number] = course_to_add

    else: working_schedule[course_number] = course_to_add

    # print(working_schedule)

    return working_schedule


def Print_Current_Schedule(schedule):
    """
    '#': {'Course Number': '#', 'Room Number': ###, 'Time Slot': #, 'Conflicts': ['#', '#', ...]}
    """
    print(schedule)
    for course in schedule:
        print(f"Course: C{course} | Time Slot: {schedule[course]['Time Slot']} | Room: {schedule[course]['Room Number']}")



if __name__ == "__main__":
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
    working_schedule = {}

    # Getting the course number
    course_num = input("\nEnter a Course Number: ")
    while course_num != "-1":
        while not(course_num.isdigit()):
            course_num = input("Please enter a digit for the Course Number: ")

        
        conflicts, conflict_types = add_course(course_num, all_conflict_types)
        course_to_add = {"Course Number": course_num, "Room Number": 100, "Time Slot": 0, "Conflicts": conflicts, "Conflict Types": conflict_types}
        working_schedule = schedule_courses(working_schedule, course_to_add)
        Print_Current_Schedule(working_schedule)

        course_num = input("\nEnter a Course Number: ")