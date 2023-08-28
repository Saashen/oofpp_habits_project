import questionary
from datetime import datetime, date
from Habit import DatabaseHabit
from db import get_db, get_creation_time, get_habit
from analytics import get_habits, get_period_habits, get_streaks_for_habits, get_streak_for_habit, \
    get_weakest_habits
from helpers import ask_for_title, ask_for_date, check_if_exists


def cli():
    """
    A function that handles the user's requests to the Command Line Interface, using the questionary library
    :return: None
    """
    db = get_db()
    questionary.confirm('Do you want to start?').ask()
    stop = False

    while not stop:
        choice = questionary.select(
            'What do you want to do?',
            choices=['Create a new habit', 'Check off the habit`s task', 'Get analytics', 'Delete the habit', 'Exit']
        ).ask()

        if choice == 'Create a new habit':
            title = ask_for_title()
            habit_to_check = get_habit(db, title)

            if habit_to_check is not None:
                print(f'The habit with the title `{title}` already exists.')
                return

            description = questionary.text('What is the description of your habit?').ask()
            periodicity = questionary.select(
                'What is the periodicity of your habit?',
                choices=['daily', 'weekly']
            ).ask()
            questionary.confirm(f'You cannot enter the habit`s creation date later than today.').ask()
            custom_date = ask_for_date()

            if custom_date > date.today():
                print('The creation date cannot be later than today!')
                return

            habit = DatabaseHabit(title, description, periodicity, custom_date)
            habit.store(db)
        elif choice == 'Check off the habit`s task':
            title = ask_for_title()

            if check_if_exists(db, title) is False:
                return

            habit = DatabaseHabit(title)
            creation_time_string = get_creation_time(db, title)[0]
            creation_time = datetime.strptime(creation_time_string, '%Y-%m-%d')
            questionary.confirm(f'You cannot enter the task completion date earlier than creation time '
                                f'`{str(creation_time)}` and later than today.').ask()
            
            custom_date = date.today()
            try:
                custom_date = ask_for_date()
                print(custom_date)
            except ValueError:
                print('The date is not valid.')
                return

            if custom_date > date.today() or custom_date < creation_time.date():
                print('The creation date cannot be earlier than creation time and later than today!')
                return

            habit.complete_task(db, custom_date)
        elif choice == 'Get analytics':
            analytics_choice = questionary.select(
                'Which kind of analytics do you want to receive?',
                choices=[
                    'List of all habits', 'List of habits with the same periodicity', 'The longest streak of a habit',
                    'The longest streak of all habits', 'Habits I struggle the most last month'
                ]
            ).ask()

            if analytics_choice == 'List of all habits':
                get_habits(db)
            elif analytics_choice == 'List of habits with the same periodicity':
                period = questionary.select(
                    'What is the periodicity of your habit?',
                    choices=['daily', 'weekly']
                ).ask()
                get_period_habits(db, period)
            elif analytics_choice == 'The longest streak of a habit':
                title = ask_for_title()

                if check_if_exists(db, title) is False:
                    return

                get_streak_for_habit(db, title)
            elif analytics_choice == 'The longest streak of all habits':
                get_streaks_for_habits(db)
            elif analytics_choice == 'Habits I struggle the most last month':
                get_weakest_habits(db)
        elif choice == 'Delete the habit':
            title = ask_for_title()

            if check_if_exists(db, title) is False:
                return

            habit = DatabaseHabit(title)
            habit.delete(db)
            del habit
        elif choice == 'Exit':
            print('See you next time!')
            stop = True
        else:
            print('No match found')


if __name__ == '__main__':
    cli()
