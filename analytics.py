from db import (
    get_habits_titles,
    get_habits_period,
    get_longest_streaks,
    get_longest_streak,
    get_all_streak_counts,
)
from Habit import Periodicity


def get_habits(db):
    """
    Print the titles of all current habits
    :param db: a database connection
    :return: None
    """
    titles = get_habits_titles(db)
    print("Habit titles are: ")
    for idx, x in enumerate(titles):
        print(f"{idx + 1}. {x[0]}", end=" \n")


def get_period_habits(db, period):
    """
    Print all habits' titles, sorted by periodicity
    :param db: a database connection
    :param period: periodicity of habits
    :return: None
    """
    habits_period = get_habits_period(db, period)
    print(f"The habits of the period `{period}` are: ")
    if len(habits_period) < 1:
        print("None")
    else:
        for idx, x in enumerate(habits_period):
            print(f"{idx + 1}. {x[0]}", end=" \n")


def get_streak_for_habit(db, title):
    """
    Print the longest run streak for each habit
    :param db: a database connection
    :param title: a habit's title
    :return: None
    """
    streak = get_longest_streak(db, title)
    print(f"Your longest streak of the habit `{title}` is: {streak[0]}")


def get_streaks_for_habits(db):
    """
    Print the longest run streaks of all habits, sorted by periodicity
    :param db: a database connection
    :return: None
    """
    print("The longest streaks of all habits are: ")
    for period in Periodicity:
        streaks = get_longest_streaks(db, period)
        sorted_streaks = sorted(streaks, key=lambda feature: feature[1], reverse=True)
        print(period)
        for idx, x in enumerate(sorted_streaks):
            print(f"{idx + 1}. {x[0]} - {x[1]}", end=" \n")


def get_weakest_habits(db):
    """
    Print the habits with the lowest current streak count from each periodicity
    :param db: a database connection
    :return: None
    """
    print("Lately you struggled the most with these habits: ")
    for period in Periodicity:
        streaks = get_all_streak_counts(db, period)
        sorted_streaks = sorted(streaks, key=lambda x: x[1])
        print(period)
        print(f"{sorted_streaks[0][0]} - {sorted_streaks[0][1]}", end=" \n")
