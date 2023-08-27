# A Habit Tracker App

A Habit Tracker App was designed to assist users in tracking their habits: store the information about habits and 
calculate the count of completed tasks of the habit. The application uses CLI (Command-Line Interface) to communicate 
with users. For that I use the questionary library. The Habit Tracker App saves the information after the end of 
the session by using sqlite3 library. 

This project uses Python version 3.9.13.

A Habit Tracker App is a continuous examination project for the Object-Oriented and Functional Programming 
with Python course.

## What does it do?

The application can:
- create habits
- check off tasks for habits
- provide analytics for habits, such as
  - list all habits
  - list all habits of a certain periodicity
  - the longest streak of a habit
  - the longest streak of all habits, sorted by periodicity
  - habits user struggled the most, sorted by periodicity
- delete habits

## Installation

```shell
pip install -r requirements.txt
```

## Usage

Start the application with

```shell
python main.py
```

and follow instructions in the terminal.

## Tests

```shell
pytest .
```

## License

MIT License

Copyright (c) 2023 Ablitsova