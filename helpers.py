from datetime import date, datetime
import questionary
from constants import invalid_value_message

from db import get_habit, get_latest_date, get_creation_time


def ask_for_title():
    """
    Ask user for a title and validate it
    :return: a questionary question
    """
    title = questionary.text(
        "What is the title of your habit?",
        validate=lambda text: True if len(text) > 0 else "Please enter a value",
    ).ask()
    return title


def ask_for_date():
    """
    Ask user for a year, a month, and a date and create the date object from them
    :return: a date object or None
    """
    year = questionary.text(
        "Year? E.g. 2023",
        default=str(date.today().year),
        validate=lambda text: True if len(text) == 4 else invalid_value_message,
    ).ask()

    month = questionary.text(
        "Month? E.g. 7",
        default=str(date.today().month),
        validate=lambda text: True if 0 < len(text) < 3 else invalid_value_message,
    ).ask()

    day = questionary.text(
        "Day? E.g. 17",
        default=str(date.today().day),
        validate=lambda text: True if 0 < len(text) < 3 else invalid_value_message,
    ).ask()

    try:
        return datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d").date()
    except ValueError:
        return


def check_if_exists(db, habit_title):
    """
    Check whether the habit with a given title exists
    :param db: a database connection
    :param habit_title: a habit's title
    :return: Boolean
    """
    if habit_title is None:
        print(invalid_value_message)
        return False
    habit_to_check = get_habit(db, habit_title)
    if habit_to_check is None:
        print(f"The habit with the title `{habit_title}` does not exist.")
        return False
    else:
        return True
