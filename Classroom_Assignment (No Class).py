import random
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
def add_course(course_num):
    return input(f"Enter the courses that conflict with C{course_num}: ").strip().split()


def schedule_courses(working_schedule, course_to_add):
    course_number = course_to_add["Course Number"]
    if len(working_schedule) != 0:
        room_number = course_to_add["Room Number"]
        time_slot = course_to_add["Time Slot"]
        conflicts = course_to_add["Conflicts"]

        for course in working_schedule:
            if (working_schedule[course]["Course Number"] in conflicts) or (course_number in working_schedule[course]["Conflicts"]):
                room_number += 1
                time_slot += 1

            if (course_to_add["Room Number"] == working_schedule[course]["Room Number"]) and (course_to_add["Time Slot"] == working_schedule[course]["Time Slot"]):
                pass

        working_schedule[course_number] = course_to_add

    else: working_schedule[course_number] = course_to_add

    # print(working_schedule)

    return working_schedule


def Print_Current_Schedule(schedule):
    """
    '#': {'Course Number': '#', 'Room Number': ###, 'Time Slot': #, 'Conflicts':['#', '#', ...]}
    """
    for course in schedule:
        print(f"Course: C{course} | Time Slot: {schedule[course]['Time Slot']} | Room: {schedule[course]['Room Number']}")



if __name__ == "__main__":
    debug_example_classes = True
    if debug_example_classes:
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
        working_schedule = {}

        course_num = input("\nEnter a Course Number: ")
        while course_num != "-1":
            while not(course_num.isdigit()):
                course_num = input("Please enter a digit for the Course Number: ")

            conflicts = add_course(course_num)
            course_to_add = {"Course Number": course_num, "Room Number": 100, "Time Slot": 0, "Conflicts": conflicts}
            working_schedule = schedule_courses(working_schedule, course_to_add)
            Print_Current_Schedule(working_schedule)

            course_num = input("\nEnter a Course Number: ")


        # C1 = Course(course_number=1, course_in_conflict=[2, 3], conflict_type=[1, 2])
        # C2 = Course(course_number=2, course_in_conflict=[1, 4], conflict_type=[1, 3])
        # C3 = Course(course_number=3, course_in_conflict=[1, 5], conflict_type=[2, 4])
        # C4 = Course(course_number=4, course_in_conflict=[2, 6], conflict_type=[3, 3])
        # C5 = Course(course_number=5, course_in_conflict=[3, 6], conflict_type=[4, 1])
        # C6 = Course(course_number=6, course_in_conflict=[4, 5], conflict_type=[3, 1])

        # for course in [C1, C2, C3, C4, C5, C6]