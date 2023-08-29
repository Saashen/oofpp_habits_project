from datetime import date
from Habit import DatabaseHabit
from analytics import (
    get_habits,
    get_period_habits,
    get_streak_for_habit,
    get_streaks_for_habits,
    get_weakest_habits,
)
from db import get_db


class TestHabit:
    def setup_method(self):
        self.db = get_db("test.db")

        daily_habit1 = DatabaseHabit(
            "test_title1", "test_description1", "daily", date(2023, 8, 1)
        )
        daily_habit1.store(self.db)
        daily_habit1.complete_task(self.db, date(2023, 8, 2))
        daily_habit1.complete_task(self.db, date(2023, 8, 3))
        daily_habit1.complete_task(self.db, date(2023, 8, 5))
        daily_habit1.complete_task(self.db, date(2023, 8, 6))

        weekly_habit1 = DatabaseHabit(
            "test_title2", "test_description2", "weekly", date(2023, 8, 2)
        )
        weekly_habit1.store(self.db)
        weekly_habit1.complete_task(self.db, date(2023, 8, 9))
        weekly_habit1.complete_task(self.db, date(2023, 8, 16))
        weekly_habit1.complete_task(self.db, date(2023, 8, 25))
        weekly_habit1.complete_task(self.db, date(2023, 9, 6))

        daily_habit2 = DatabaseHabit(
            "test_title3", "test_description3", "daily", date(2023, 8, 3)
        )
        daily_habit2.store(self.db)
        daily_habit2.complete_task(self.db, date(2023, 8, 4))
        daily_habit2.complete_task(self.db, date(2023, 8, 6))
        daily_habit2.complete_task(self.db, date(2023, 8, 7))
        daily_habit2.complete_task(self.db, date(2023, 8, 8))

        weekly_habit2 = DatabaseHabit(
            "test_title4", "test_description4", "weekly", date(2023, 8, 4)
        )
        weekly_habit2.store(self.db)
        weekly_habit2.complete_task(self.db, date(2023, 8, 11))
        weekly_habit2.complete_task(self.db, date(2023, 8, 18))
        weekly_habit2.complete_task(self.db, date(2023, 8, 25))
        weekly_habit2.complete_task(self.db, date(2023, 9, 1))

    def test_habit_class_instance(self, capsys):
        habit = DatabaseHabit(
            "test_title5", "test_description5", "weekly", date(2023, 8, 5)
        )
        habit.store(self.db)
        captured = capsys.readouterr()
        assert (
            captured.out
            == "The habit with the title `test_title5` was successfully added.\n"
        )

        habit.complete_task(self.db, date(2023, 8, 12))
        captured = capsys.readouterr()
        assert (
            captured.out
            == "The successful streak count was updated.\nYou have a new record! Your longest streak for the habit `test_title5` is 1.\n"
        )

        habit.complete_task(self.db, date(2023, 8, 19))
        captured = capsys.readouterr()
        assert (
            captured.out
            == "The successful streak count was updated.\nYou have a new record! Your longest streak for the habit `test_title5` is 2.\n"
        )

        habit.complete_task(self.db, date(2023, 8, 27))
        captured = capsys.readouterr()
        assert (
            captured.out
            == "You broke your habit! You skipped more than 7 day(s)\nThe successful streak count was updated.\n"
        )

        habit.delete(self.db)
        captured = capsys.readouterr()
        assert (
            captured.out
            == "The completed tasks of the habit `test_title5` were successfully deleted.\nThe habit with the title `test_title5` was successfully deleted.\n"
        )

    def test_analytics(self, capsys):
        get_habits(self.db)
        captured = capsys.readouterr()
        assert (
            captured.out
            == "Your current habits are: \n1. test_title1: test_description1 \n2. test_title2: test_description2 \n3. test_title3: test_description3 \n4. test_title4: test_description4 \n"
        )

        get_period_habits(self.db, "daily")
        captured = capsys.readouterr()
        assert (
            captured.out
            == "The habits of the period `daily` are: \n1. test_title1 \n2. test_title3 \n"
        )

        get_streak_for_habit(self.db, "test_title4")
        captured = capsys.readouterr()
        assert captured.out == "Your longest streak of the habit `test_title4` is: 4\n"

        get_streaks_for_habits(self.db)
        captured = capsys.readouterr()
        assert (
            captured.out
            == "The longest streaks of all habits are: \ndaily\n1. test_title3 - 3 \n2. test_title1 - 2 \nweekly\n1. test_title4 - 4 \n2. test_title2 - 2 \n"
        )

        get_weakest_habits(self.db)
        captured = capsys.readouterr()
        assert (
            captured.out
            == "Lately you struggled the most with these habits: \ndaily\ntest_title1: the current streak count is 2 \nweekly\ntest_title2: the current streak count is 1 \n"
        )

    def teardown_method(self):
        import os

        self.db.close()
        os.remove("test.db")
