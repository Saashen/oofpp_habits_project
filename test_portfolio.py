from Habit import DatabaseHabit
from db import get_db, add_habit, add_completed_task, get_completed_tasks


class TestHabit:
    def setup_method(self):
        self.db = get_db('test.db')

        add_habit(self.db, 'test_title', 'test_description')
        add_completed_task(self.db, 'test_title', '2023-06-20')
        add_completed_task(self.db, 'test_title', '2023-06-21')
        add_completed_task(self.db, 'test_title', '2023-06-23')
        add_completed_task(self.db, 'test_title', '2023-06-24')

    def test_habit(self):
        habit = DatabaseHabit('test_title4', 'test_description1', 'weekly')
        habit.store(self.db)

        habit.complete_task()
        habit.add_task(self.db)
        habit.streak_break()
        habit.complete_task()
        habit.show_completed_tasks()

    def test_db_habit(self):
        # test get_habits and get_habits_titles
        # test get_period_habits and get_habits_period
        data = get_completed_tasks(self.db, 'test_title')
        assert len(data) == 4

    def teardown_method(self):
        import os
        self.db.close()
        os.remove('test.db')
