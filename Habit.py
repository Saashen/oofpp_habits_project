from datetime import timedelta, date, datetime
from db import (
    add_habit,
    add_completed_task,
    delete_habit,
    get_creation_time,
    get_latest_date,
    get_streak_count,
    get_longest_streak,
    get_periodicity,
    update_streak_count,
    update_longest_streak,
    reset_streak_count,
    delete_completed_tasks,
)
from constants import Periodicity


class Habit:
    def __init__(
        self,
        title: str,
        description: str = "",
        periodicity: Periodicity = "daily",
        creation_time: date = date.today(),
    ):
        """Habit class, to create a habit
        :param title: a habit's title
        :param description: a habit's description
        :param periodicity: how often the habit should be performed
        :param creation_time: a date of habit's creation
        """
        self.title = title
        self.description = description
        self.periodicity = periodicity
        self.creation_time = creation_time

    def __str__(self):
        """
        Return the information about the current instance
        :return: a sting
        """
        return (
            f"title: {self.title}\ndescription: {self.description}\nperiodicity: {self.periodicity}\n"
            f"creation_time: {self.creation_time} "
        )


class DatabaseHabit(Habit):
    def store(self, db):
        """
        Dispatch habit's data to add the habit to the database
        :param db: a database connection
        :return: None
        """
        add_habit(
            db, self.title, self.description, self.periodicity, self.creation_time
        )

    def complete_task(self, db, custom_date):
        """
        Add a completed task to the database, update the streak count and the longest streak, inform the user about
         progress
        :param db: a database connection
        :param custom_date: a date that was defined by user
        :return: None
        """
        streak_count = get_streak_count(db, self.title)[0]
        longest_streak = get_longest_streak(db, self.title)[0]
        periodicity = get_periodicity(db, self.title)[0]
        creation_time_string = get_creation_time(db, self.title)[0]
        periodicity_days = 1 if periodicity == "daily" else 7
        latest_date_string = get_latest_date(db, self.title)[0]

        if latest_date_string is None:
            latest_date_string = creation_time_string
        else:
            if latest_date_string == custom_date.strftime("%Y-%m-%d"):
                print("You have already completed this task on this day.")
                return

        latest_date = datetime.strptime(latest_date_string, "%Y-%m-%d").date()

        if custom_date - timedelta(days=periodicity_days) <= latest_date:
            update_streak_count(db, self.title, streak_count)
            print(f"The successful streak count was updated.")
            if streak_count + 1 > longest_streak:
                update_longest_streak(db, self.title, longest_streak)
                print(
                    f"You have a new record! Your longest streak for the habit `{self.title}` is {streak_count + 1}."
                )
        else:
            print(
                f"You broke your habit! You skipped more than {timedelta(days=periodicity_days).days} day(s)"
            )
            reset_streak_count(db, self.title)
            print(f"The successful streak count was updated.")

        add_completed_task(db, self.title, custom_date)
        db.commit()

    def delete(self, db):
        """
        Dispatch the habit's data to delete the habit in the database
        :param db: a database connection
        :return: None
        """
        delete_completed_tasks(db, self.title)
        delete_habit(db, self.title)
