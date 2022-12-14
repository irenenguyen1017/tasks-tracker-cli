import os

__app_name__ = "tasks-tracker"
__author__ = "Irene Nguyen"
__version__ = "0.1.0"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, "tasks-tracker.db")

DISPLAYING_DATE_FORMAT = "%d/%m/%Y"
DB_DATE_FORMAT = "%Y-%m-%d"

NO_TASK_FOUND = "No task found!"
DATA_CONNECTION_ERROR = "Something wrong with database. Please try again."
ADDING_TASK_SUCCESS = "New task added successfully."
ADDING_TASK_ERROR = "Adding task failed. Please try again."
NO_TASK_FOUND_ERROR = "Cannot find any task with provided ID."
UPDATE_TASK_SUCCESS = "Task updated successfully."
UPDATE_TASK_ERROR = "Updating task failed. Please try again."
DELETE_TASK_SUCCESS = "Task deleted successfully."
DELETE_TASK_ERROR = "Deleting task failed. Please try again."
DELETE_ALL_TASKS_SUCCESS = "All tasks deleted successfully."
DELETE_ALL_TASKS_ERROR = "Deleting all tasks failed. Please try again."
