import os
import datetime
import sys

from peewee import *

db = SqliteDatabase("wl.db")


class Entry(Model):
    my_name = CharField(max_length=100)
    task_name = CharField(max_length=100)
    minutes = IntegerField(default=0)
    notes = CharField(max_length=200)
    created_at = DateTimeField(default=datetime.datetime.now)

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


# ###############################
# menu functions below


def menu_loop():
    """main menu loop & get option from it"""
    while True:
        menu_option = input("""
            1- New entry
            2- Find previous entry
            3- Save and quit
>>> """)
        if menu_option in ["1", "2", "3"]:
            if menu_option == "1":
                clear()
                create_entry()
            elif menu_option == "2":
                find_previous()
            elif menu_option == "3":
                sys.exit()
        else:
            print("Enter a valid option [1, 2, 3]")
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
    wait()


# Find Previous Functions
# ---------------------------
def find_previous():
    """find previous entries"""
    while True:
        menu_option = input("""
            1- Find by employee
            2- Find by date
            3- Find by time spent
            4- Find by search term
            5- Find by date range
            6- Return back to main menu
>>> """)
        entry = ""
        if menu_option in ["1", "2", "3", "4", "5", "6"]:
            if menu_option == "1":
                entry = find_by_employee()
            elif menu_option == "2":
                entry = find_by_date()
            elif menu_option == "3":
                entry = find_by_time()
            elif menu_option == "4":
                entry = find_by_search_term()
            elif menu_option == "5":
                entry = find_by_date_range()
            elif menu_option == "6":
                clear()
                break

            if entry:
                edit_delete_entry(entry)
        else:
            print("Enter a valid option [1, 2, 3, 4, 5, 6]")
            wait()


def find_by_employee():
    """find entry by employee name"""
    name = input("Enter employee name >>> ").strip()
    if name:
        clear()
        entries = Entry.select()
        if entries:
            entries_found = Entry.select().where(Entry.my_name == name)
            if entries_found:
                return get_entry_from_entries(entries_found)
        else:
            print("No entries were found")
            input("Press Enter to go back to main menu... ")
            clear()
    else:
        print("Enter a valid input")
        input("Press Enter to continue... ")
        clear()


def find_by_date():
    """find entry based on user's input date format"""
    while True:
        date_format = input("Enter date in this "
                            "format mm/dd/yyyy >>> ").strip()
        try:
            date = datetime.datetime.strptime(date_format, "%m/%d/%Y")
            break
        except ValueError:
            print("Please enter a valid date in this form: mm/dd/yyyy")
    entries_found = Entry.select().where(
                            Entry.created_at.year == date.year,
                            Entry.created_at.month == date.month,
                            Entry.created_at.day == date.day)
    if entries_found:
        clear()
        return get_entry_from_entries(entries_found)
    else:
        print("No entries were found")
        wait()


def find_by_time():
    """find entry based on number of minutes user has entered"""
    while True:
        minutes = input("Enter time spent of entry >>> ")
        if minutes:
            try:
                minutes = int(minutes)
                break
            except ValueError:
                print("Please enter a valid input. ex 12")
                wait()
        else:
            print("Please enter a valid input. ex: 12")
            wait()

    if minutes:
        entries_found = Entry.select().where(Entry.minutes == minutes)
        if entries_found:
            return get_entry_from_entries(entries_found)
        else:
            print("No entries were found based on your search")
            wait()


def find_by_search_term():
    """find an entry based on a keyword found in notes or task_name"""
    while True:
        keyword = input("Enter search term >>> ")
        if keyword:
            entries_found = Entry.select().where(
                            (Entry.task_name.contains("%{}%".format(keyword)))
                            | (Entry.notes.contains("%{}%".format(keyword))))
            break
        else:
            print("Please enter a valid input")
            wait()

    if entries_found:
        return get_entry_from_entries(entries_found)
    else:
        print("No entries were found based on your search")
        wait()


def find_by_date_range():
    """find by date range For example between 01/01/2016 and 12/31/2016."""
    # user should enter a valid date
    # first date
    while True:
        first_date_format = input("Enter the first date mm/dd/yyyy >>> ")
        try:
            first_date = datetime.datetime.strptime(first_date_format,
                                                    "%m/%d/%Y")
            break
        except ValueError:
            print("Please enter a valid date")
            print("Press Enter to continue")
            clear()

    # second date
    while True:
        second_date_format = input("Enter the second date mm/dd/yyyy >>> ")
        try:
            second_date = datetime.datetime.strptime(second_date_format,
                                                     "%m/%d/%Y")
            break
        except ValueError:
            print("Please enter a valid date")

    # calculate number of dates between first and second dates
    days = (second_date - first_date).days
    # array of all dates between the first and second dates
    dates = []
    for i in range(1, days+1):
        dates.append(first_date + datetime.timedelta(days=i))
    entries_found = Entry.select().where(
                            Entry.created_at.between(dates[0], dates[-1]))
    if entries_found:
        return get_entry_from_entries(entries_found)
    else:
        print("no entries were found based on your search")
        wait()


def get_entry_from_entries(entries_found):
    """go through entries(next/previous) and choose one."""
    clear()
    entries_found = list(enumerate(entries_found))
    count = 0
    while True:
        display_entry(entries_found[count])
        entry = input("N: next. P: previous. Enter: choose entry >>> ")
        if entry.lower() == "n":
            if count == len(entries_found) - 1:
                print("This is the last entry")
                wait()
            elif count < len(entries_found) - 1:
                count += 1
                clear()
        elif entry.lower() == "p":
            if count == 0:
                print("This is the first entry")
                wait()
            elif count > 0:
                count -= 1
                clear()
        elif entry == "":
            clear()
            return entries_found[count]


# Editing Fucntions
# ---------------------------------------

def edit_delete_entry(entry):
    """choose whether to edit or delete an entry"""
    while True:
        display_entry(entry)
        menu_option = input("""
            1- Edit entry
            2- Delete entry
            3- Return back
>>> """)
        if menu_option in ["1", "2", "3"]:
            if menu_option == "1":
                clear()
                edit_entry(entry)
                break
            elif menu_option == "2":
                entry[1].delete_instance()
                print("Entry deleted")
                wait()
                break
            elif menu_option == "3":
                break
        else:
            print("Please enter a valid option [1,2]")
            wait()


def edit_entry(entry):
    """contains a menu of several editing options"""
    while True:
        display_entry(entry)
        menu_option = input("""
            1- Change date
            2- Change task name
            3- Change time spent
            4- Change/Create notes
            5- Return back
>>> """)
        if menu_option in ["1", "2", "3", "4", "5"]:
            if menu_option == "1":
                change_date(entry[1])
            if menu_option == "2":
                change_task_name(entry[1])
            elif menu_option == "3":
                change_time_spent(entry[1])
            elif menu_option == "4":
                change_notes(entry[1])
            if menu_option == "5":
                clear()
                break
        else:
            print("Please enter a valid option [1,2,3,4,5]")


def change_date(entry):
    """let the user change the date of the passed entry"""
    while True:
        new_date_format = input("Enter your new date mm/dd/yyyy >>> ")
        if new_date_format:
            try:
                new_date = datetime.datetime.strptime(new_date_format,
                                                      "%m/%d/%Y")
                entry.created_at = new_date
                entry.save()
                clear()
                break
            except ValueError:
                print("Please enter a valid date format. ex 01/20/2013")
        else:
            print("Please enter an input. ex 01/20/2013")


def change_task_name(entry):
    while True:
        new_task_name = input("Enter the new task name >>> ")
        if new_task_name:
            entry.task_name = new_task_name
            entry.save()
            clear()
            break
        else:
            print("Please enter an input")


def change_time_spent(entry):
    while True:
        new_time_spent = input("Enter the new time spent in minutes >>> ")
        if new_time_spent:
            try:
                new_time_spent = int(new_time_spent)
                entry.minutes = new_time_spent
                entry.save()
                clear()
                break
            except ValueError:
                print("Please enter a valid input. ex: 12")
        else:
            print("Please enter an input")


def change_notes(entry):
    while True:
        new_note = input("Enter the new note >>> ")
        if new_note:
            entry.notes = new_note
            entry.save()
            clear()
            break
        else:
            print("Please enter an input")

# helper functions
# -----------------------------------


def display_entry(entry):
    """display entry in a good format"""
    print()
    print(str(entry[0]) + ")")
    print()
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
