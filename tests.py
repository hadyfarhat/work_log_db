import unittest

from work_log import *

def testing(test_name, solution):
    clear()
    print("Testing {}... enter {}".format(test_name, solution))

class TestWorkLog(unittest.TestCase):
    def setUp(self):
        # db.connect()
        db.create_tables([Entry], safe=True)
        self.e = Entry(my_name="hadi",
                       task_name="task 1",
                       minutes=12,
                       notes="")
        self.e.save()

    def tearDown(self):
        Entry.delete().execute()

    def test_create_entry(self):
        testing("create_entry()", "hadi as name")
        create_entry()
        entry = Entry.select().where(Entry.my_name == "hadi")
        self.assertTrue(entry)

    def test_find_by_employee(self):
        testing("find_by_employee", "hadi")
        entry = find_by_employee()
        self.assertEqual(entry[1].my_name, "hadi")

    def test_find_by_date(self):
        testing("find_by_date()", "04/22/2017")
        entry = find_by_date()
        self.assertEqual(entry[1].my_name, "hadi")

    def test_find_by_search_term(self):
        testing("find_by_search_term()", "task 1")
        entry = find_by_search_term()
        self.assertEqual(entry[1].my_name, "hadi")

    def test_find_by_date_range(self):
        testing("find_by_date_range", "04/21/2017, 04/23/2017")
        entry = find_by_date_range()
        self.assertEqual(entry[1].my_name, "hadi")

    def test_change_task_name(self):
        testing("change_task_name()", "task 11")
        change_task_name(self.e)
        entry = Entry.get(Entry.task_name == "task 11")
        self.assertTrue(entry)

    def test_change_date(self):
        testing("change_date()", "10/20/1997")
        change_date(self.e)
        entry = Entry.get(Entry.created_at.year == 1997)
        self.assertTrue(entry)

    def test_change_time_spent(self):
        testing("change_time_spent", "7")
        change_time_spent(self.e)
        entry = Entry.get(Entry.minutes == 7)
        self.assertTrue(entry)

    def test_change_notes(self):
        testing("change_notes()", "note 7")
        change_notes(self.e)
        entry = Entry.get(Entry.notes == "note 7")
        self.assertTrue(entry)


if __name__ == "__main__":
    unittest.main()
