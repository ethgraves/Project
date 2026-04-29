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
    if course_num not in working_schedule["Courses"]:
        working_schedule["Courses"].append(course_num)
        working_schedule["Time and Room"][course_num] = [1, 100]
        working_schedule["Conflicts and Conflict Types"][course_num] = {}

    for i in range(len(course_conflicts)):
        conflicted_course = course_conflicts[i]
        conflicted_course_type = conflict_types[i]

        working_schedule["Conflicts and Conflict Types"][course_num][conflicted_course] = conflicted_course_type

        if conflicted_course not in working_schedule["Courses"]:
            working_schedule["Courses"].append(conflicted_course)
            working_schedule["Time and Room"][conflicted_course] = [1, 100]
            working_schedule["Conflicts and Conflict Types"][conflicted_course] = {}

        working_schedule["Conflicts and Conflict Types"][conflicted_course][course_num] = conflicted_course_type



def Add_Course(course_num, all_conflict_types, working_schedule, counter=0):
    course_conflicts = []
    conflict_types = []

    while True:
        counter += 1

        # =========================
        # GETTING COURSE CONFLICTS
        # =========================
        if counter == 1:
            print('\n=========================================')
            print('If there are no conflicts, enter "None"')
            print('=========================================', end='')
            
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


        # ======================
        # GETTING CONFLICT TYPES
        # ======================
        print("\nTYPES OF CONFLICT:",
            "\n 1. Courses have the Same Professor"
            "\n 2. Courses have the Same Room Number"
            "\n 3. Courses have the Same Time Slot"
            "\n 4. Courses have the Same Students"
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


def Schedule_Courses(working_schedule, num_time_slots, num_rooms):
    print_schedule = True
    conflicts_present = True
    total_number_of_slots = num_time_slots * num_rooms

    if len(working_schedule["Courses"]) == 0:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Please add courses first")
        print("!!!!!!!!!!!!!!!!!!!!!!!!\n")
        print_schedule = False
        return working_schedule, print_schedule

    if len(working_schedule["Courses"]) > total_number_of_slots:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Not enough Time Slots and Rooms available for all courses")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        print_schedule = False
        return working_schedule, print_schedule
    

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
    
    return working_schedule, print_schedule


def Print_Current_Schedule(schedule):
    print("\n=================================================")
    print("FULL SCHEDULE:\n")
    for course in schedule["Courses"]:
        print(f"Course: C{course} | Time Slot: {schedule['Time and Room'][course][0]} | Room: {schedule['Time and Room'][course][1]}")
    print("=================================================")


def View_Course_Conflicts(working_schedule):
    while True:
        print("Here are the courses:")
        for course in range(len(working_schedule["Courses"])):
            print(f"   * Course {working_schedule['Courses'][course]}")
        course_to_edit = input("\nWhich course would you like to view the conflicts of: ").strip().lower()
        while course_to_edit not in working_schedule["Courses"]:
            course_to_edit = input("That is not a course. Which course would you like to edit: ").strip().lower()

        print(f"\nCourse {course_to_edit} Conflicts:")
        for conflict in working_schedule["Conflicts and Conflict Types"][course_to_edit]:
            course_conflicts = []
            conflict_types = []
            course_conflicts.append(conflict)
            conflict_types.append(working_schedule["Conflicts and Conflict Types"][course_to_edit][conflict])
            print(f"    * Course {conflict} (with conflict type #{working_schedule['Conflicts and Conflict Types'][course_to_edit][conflict]})\n")
    
        view_more_courses = input("Would you like to view another course (Yes or No)? ").strip().lower()
        while view_more_courses not in ["yes", "y", "no", "n"]:
            view_more_courses = input("That is not an option. Would you like to view another course? (Yes or No)").strip().lower()

        if view_more_courses in ["yes", "y"]:
            continue
        elif view_more_courses in ["no", "n"]:
            break
        else:
            print("!!! ERROR OCCURRED !!!")


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

    num_time_slots = input("How many Time Slots are available? ").strip().lower()
    while not(num_time_slots.isdigit()):
        num_time_slots = input("Please enter a digit for the Number of Available Time Slots: ").strip().lower()

    num_rooms = input("How many Rooms are available? ").strip().lower()
    while not(num_rooms.isdigit()):
        num_rooms = input("Please enter a digit for the Number of Available Rooms: ").strip().lower()

    num_time_slots = int(num_time_slots)
    num_rooms = int(num_rooms)

    # Getting the course number
    while True:
        print("\n=================================================")
        print(f"OPTIONS\n"
               "-------"
               "\n  1. Add/Edit a Course"
               "\n  2. View Course's Conflicts"
               "\n  3. Change the Number of Available Time Slots"
               "\n  4. Change the Number of Available Rooms"
               "\n  5. Print Current Schedule"
               "\n  6. Quit")
        option = input("\nChoose one of the above options: ").strip().lower()
        while option not in ["1", "2", "3", "4", "5", "6"]:
            option = input("That is not an option. Please choose one of the above options: ").strip().lower()

        if option == "1":
            course_num = input("\nEnter a course number: ").strip().lower()
            while not(course_num.isdigit()):
                course_num = input("Please enter a digit for a Course Number: ").strip().lower()
            working_schedule = Add_Course(course_num, all_conflict_types, working_schedule)

        elif option == "2":
            View_Course_Conflicts(working_schedule)

        elif option == "3":
            print(f"Current Number of Available Time Slots: {num_time_slots}")
            num_time_slots = input("How many Time Slots are available? ").strip().lower()
            while not(num_time_slots.isdigit()):
                num_time_slots = input("Please enter a digit for the Number of Available Time Slots: ").strip().lower()
            num_time_slots = int(num_time_slots)

        elif option == "4":
            print(f"Current Number of Available Rooms: {num_rooms}")
            num_rooms = input("How many Rooms are available? ").strip().lower()
            while not(num_rooms.isdigit()):
                num_rooms = input("Please enter a digit for the Number of Available Rooms: ").strip().lower()
            num_rooms = int(num_rooms)

        elif option == "5":
            working_schedule, print_schedule = Schedule_Courses(working_schedule, num_time_slots, num_rooms)
            if print_schedule: Print_Current_Schedule(working_schedule)
        
        elif option == "6":
            break


if __name__ == "__main__":
    DEBUG_MODE = False

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