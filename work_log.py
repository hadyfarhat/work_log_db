import os
import datetime

from peewee import *

db = SqliteDatabase("wl.db")


class Entry(Model):
    my_name = CharField(max_length=100)
    task_name = CharField(max_length=100)
    minutes = IntegerField(default=0)
    notes = CharField(max_length=200)
    created_at = DateTimeField(defualt=datetime.datetime.now)

    class Meta:
        database = db


def get_name():
    """get name of user"""
    while True:
        name = input("Enter your name >>> ")
        if name:
            if len(name) > 100:
                print("Name should be less than 100")
            else:
                return name
        else:
            print("Please enter a valid input")


def get_task_name():
    """get task_name"""
    while True:
        task_name = input("Enter the task name >>> ")
        if task_name:
            if len(task_name) > 100:
                print("Task Name should be less than 100")
            else:
                return task_name
        else:
            print("Please enter a valid input")


def get_minutes():
    """get num of minutes"""
    while True:
        minutes = input("Enter num of minutes >>> ")
        try:
            minutes = int(minutes)
            return minutes
        except ValueError:
            print("Enter a valid number of minutes. ex: 12")


def get_notes():
    """get notes (optional)"""
    while True:
        notes = input("Enter a note or a space to leave blank >>> ")
        if notes:
            if len(notes) > 200:
                print("Please enter a note < 200 chars")
                input("Press Enter to continue... ")
                clear()
            else:
                return notes
        else:
            return ""


#------------------------------------------------
# menu functions below


def menu_loop():
    """main menu loop & get option from it"""
    while True:
        menu_option = input("""
            1- New entry
            2- Find previous entry
>>> """)
        if menu_option in ["1", "2"]:
            if menu_option == "1":
                clear()
                create_entry()
            elif menu_option == "2":
                find_previous()
        else:
            print("Enter a valid option [1, 2]")
            wait()


def create_entry():
    """create entry and save it to the database"""
    name = get_name()
    task_name = get_task_name()
    minutes = get_minutes()
    notes = get_notes()
    Entry.create(my_name=name,
                 task_name=task_name,
                 minutes=minutes,
                 notes=notes)


def find_previous():
    """find previous entries"""
    while True:
        menu_option = input("""
            1- Find by employee
            2- Find by date
            3- Find by time spent
            4- Find by search term
            5- Return back to main menu
>>> """)
        if menu_option in ["1", "2", "3", "4", "5"]:
            if menu_option == "1":
                find_by_employee()
            elif menu_option == "5":
                clear()
                break
        else:
            print("Enter a valid option [1, 2, 3, 4, 5]")
            wait()


# Find Previous Functions
#---------------------------
def find_by_employee():
    """find entry by employee name"""
    name = input("Enter employee name >>> ").strip()
    if name:
        clear()
        entries = Entry.select()
        if entries:
            entries_found = Entry.select().where(Entry.my_name == name)
            if entries_found:
                entries_found = list(enumerate(entries_found))
                while True:
                    for entry in entries_found:
                        display_entry(entry)
                    menu_option = input("Select one of the above >>> ")
                    try:
                        menu_option = int(menu_option)
                        if menu_option in range(len(entries_found)):
                            clear()
                            display_entry(entries_found[menu_option])
                            wait()
                            break
                    except ValueError:
                        print("Please enter a valid number")
                        wait()
        else:
            print("No entries were found")
            input("Press Enter to go back to main menu... ")
            clear()
    else:
        print("Enter a valid input")
        input("Press Enter to continue... ")
        clear()


def display_entry(entry):
    print()
    print(entry[0])
    print("Employee name: {}".format(entry[1].my_name))
    print("Task Name: {}".format(entry[1].task_name))
    print("Time Spent (in minutes): {}".format(entry[1].minutes))
    if entry[1].notes:
        print("Notes: {}".format(entry[1].notes))
    else:
        print("Notes: None")
    print(20*"-")
    print()


def wait():
    input("Press Enter to continue... ")
    clear()


def clear():
    os.system('cls' if 'nt' in os.name else 'clear')


if __name__ == "__main__":
    db.connect()
    db.create_tables([Entry], safe=True)
    menu_loop()









