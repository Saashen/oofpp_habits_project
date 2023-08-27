from datetime import date, datetime
import questionary

from db import get_habit, get_latest_date, get_creation_time


def ask_for_title():
    """
    Ask user for a title and validate it
    :return: a questionary question
    """
    title = questionary.text(
        'What is the title of your habit?',
        validate=lambda text: True if len(text) > 0 else 'Please enter a value'
    ).ask()
    return title


def ask_for_date():
    """
    Ask user for a year, a month, and a date and create the date object from them
    :return: a date object
    """
    year = questionary.text(
        'Year? E.g. 2023',
        default=str(date.today().year),
    ).ask()
    month = questionary.text(
        'Month? E.g. 7',
        default=str(date.today().month),
    ).ask()
    day = questionary.text(
        'Day? E.g. 17',
        default=str(date.today().day),
    ).ask()
    return datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()


def check_if_exists(db, habit_title):
    """
    Check whether the habit with a given title exists
    :param db: a database connection
    :param habit_title: a habit's title
    :return: Boolean
    """
    habit_to_check = get_habit(db, habit_title)
    if habit_to_check is None:
        print(f'The habit with the title `{habit_title}` does not exist.')
        return False
    else:
        return True


def define_latest_date(db, habit_title):
    """
    If exists, return the latest completed task of a habit, otherwise return the creation time of a habit
    :param db: a database connection
    :param habit_title: a habit's title
    :return: a date object
    """
    latest_date_string = get_latest_date(db, habit_title)[0]
    if latest_date_string is None:
        latest_date_string = get_creation_time(db, habit_title)[0]
    latest_date = datetime.strptime(latest_date_string, '%Y-%m-%d').date()
    return latest_date
