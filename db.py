import sqlite3
from datetime import date


def get_db(name="main.db"):
    """
    Create a connection to the database and initialize tables
    :param name: name of the database
    :return: a database connection
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Create habit and completed task tables if they do not exist
    :param db: a database connection
    :return: None
    """
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS habit (
        title TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT,
        streak_count INT,
        longest_streak INT,
        creation_time TEXT
    )"""
    )

    cur.execute(
        """CREATE TABLE IF NOT EXISTS completed_task (
        date TEXT,
        habit_title TEXT,
        FOREIGN KEY (habit_title) REFERENCES habit(title)
    )"""
    )

    db.commit()


def add_habit(
    db, title, description="", periodicity="daily", creation_time=date.today()
):
    """
    Add a habit to the database
    :param db: a database connection
    :param title: a habit's title
    :param description: a habit's description
    :param periodicity: a habit's periodicity
    :param creation_time: a creation time of the habit
    :return: None
    """
    cur = db.cursor()
    streak_count = 0
    longest_streak = 0
    cur.execute(
        "INSERT INTO habit VALUES (?, ?, ?, ?, ?, ?)",
        (title, description, periodicity, streak_count, longest_streak, creation_time),
    )
    print(f"The habit with the title `{title}` was successfully added.")
    db.commit()


def delete_completed_tasks(db, habit_title):
    """
    Delete completed tasks of a given habit
    :param db: a database connection
    :param habit_title: a habit's title
    :return: None
    """
    cur = db.cursor()
    cur.execute("DELETE FROM completed_task WHERE habit_title=?", (habit_title,))
    print(
        f"The completed tasks of the habit `{habit_title}` were successfully deleted."
    )
    db.commit()


def delete_habit(db, habit_title):
    """
    Delete the habit
    :param db: a database connection
    :param habit_title: a habit's title
    :return: None
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE title=?", (habit_title,))
    print(f"The habit with the title `{habit_title}` was successfully deleted.")
    db.commit()


def get_habit(db, title):
    """
    Return a habit of a given habit
    :param db: a database connection
    :param title: a habit's title
    :return: a habit
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit WHERE title=?", (title,))
    return cur.fetchone()


def get_habits_titles(db):
    """
    Return titles of all habits from the database
    :param db: a database connection
    :return: titles of all habits
    """
    cur = db.cursor()
    cur.execute("SELECT title FROM habit")
    return cur.fetchall()


def get_habits_period(db, periodicity):
    """
    Return habits of a given periodicity
    :param db: a database connection
    :param periodicity: a habit's periodicity
    :return: titles of habits
    """
    cur = db.cursor()
    cur.execute("SELECT title FROM habit WHERE periodicity=?", (periodicity,))
    return cur.fetchall()


def get_completed_tasks(db, habit_title):
    """
    Return all completed tasks of a habit from the database if habit exists
    :param db: a database connection
    :param habit_title: a habit's title
    :return: all completed tasks of a habit or a message that such a habit does not exist
    """
    cur = db.cursor()
    does_exist = cur.execute(
        "SELECT EXISTS (SELECT * FROM completed_task WHERE habit_title=?)",
        (habit_title,),
    )
    if does_exist:
        cur.execute("SELECT * FROM completed_task WHERE habit_title=?", (habit_title,))
        return cur.fetchall()
    else:
        return f"There is no habit with title {habit_title}"


def get_streak_count(db, title):
    """
    Return a streak count of a given habit
    :param db: a database connection
    :param title: a habit's title
    :return: streak count of a habit
    """
    cur = db.cursor()
    cur.execute("SELECT streak_count FROM habit WHERE title=?", (title,))
    return cur.fetchone()


def get_all_streak_counts(db, periodicity):
    """
    Return streak count of all habits of a given periodicity
    :param db: a database connection
    :param periodicity: a habit's periodicity
    :return: title, streak count, periodicity of habits
    """
    cur = db.cursor()
    cur.execute(
        "SELECT title, streak_count, periodicity FROM habit WHERE periodicity=?",
        (periodicity,),
    )
    return cur.fetchall()


def get_longest_streak(db, title):
    """
    Return the longest streak of a given habit
    :param db: a database connection
    :param title: a habit's title
    :return: longest streak of a habit
    """
    cur = db.cursor()
    cur.execute("SELECT longest_streak FROM habit WHERE title=?", (title,))
    return cur.fetchone()


def get_longest_streaks(db, periodicity):
    """
    Return longest streak of habits of a given periodicity
    :param db: a database connection
    :param periodicity: a habit's periodicity
    :return: title, longest streak, periodicity of habits
    """
    cur = db.cursor()
    cur.execute(
        "SELECT title, longest_streak, periodicity FROM habit WHERE periodicity=?",
        (periodicity,),
    )
    return cur.fetchall()


def get_latest_date(db, title):
    """
    Return the latest completed task of a given habit
    :param db: a database connection
    :param title: a habit's title
    :return: the date of completed task
    """
    cur = db.cursor()
    cur.execute("SELECT MAX (date) FROM completed_task WHERE habit_title=?", (title,))
    return cur.fetchone()


def get_creation_time(db, title):
    """
    Return creation time of a given habit
    :param db: a database connection
    :param title: a habit's title
    :return: creation time of habit
    """
    cur = db.cursor()
    cur.execute("SELECT creation_time FROM habit WHERE title=?", (title,))
    return cur.fetchone()


def get_periodicity(db, title):
    """
    Return periodicity of a given habit
    :param db: a database connection
    :param title: a habit's title
    :return: periodicity of a habit
    """
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habit WHERE title=?", (title,))
    return cur.fetchone()


def update_streak_count(db, habit_title, streak_count):
    """
    Update a streak count of a habit
    :param db: a database connection
    :param habit_title: a habit's title
    :param streak_count: a habit's streak count
    :return: None
    """
    cur = db.cursor()
    cur.execute(
        "UPDATE habit SET streak_count=? WHERE title=?", (streak_count + 1, habit_title)
    )
    db.commit()


def reset_streak_count(db, habit_title):
    """
    Set a streak count of a habit to 1
    :param db: a database connection
    :param habit_title: a habit's title
    :return: None
    """
    cur = db.cursor()
    cur.execute("UPDATE habit SET streak_count=? WHERE title=?", (1, habit_title))
    db.commit()


def update_longest_streak(db, habit_title, longest_streak):
    """
    Update the longest streak of a habit
    :param db: a database connection
    :param habit_title: a habit's title
    :param longest_streak: the longest streak of a habit
    :return: None
    """
    cur = db.cursor()
    cur.execute(
        "UPDATE habit SET longest_streak=? WHERE title=?",
        (longest_streak + 1, habit_title),
    )
    db.commit()


def add_completed_task(db, habit_title, today_date):
    """
    Add the completed task to the database
    :param db: a database connection
    :param habit_title: a habit's title
    :param today_date: a date of the completed task
    :return: None
    """
    cur = db.cursor()
    cur.execute("INSERT INTO completed_task VALUES (?, ?)", (today_date, habit_title))
    db.commit()
