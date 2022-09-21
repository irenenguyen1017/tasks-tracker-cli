from sqlite3 import Connection, Cursor, connect

from tasks_tracker.configs import DATA_CONNECTION_ERROR
from tasks_tracker.model import Task

# from tasks_tracker.typing import Priority, Status
from tasks_tracker.utils import print_error


class TasksTrackerData:
    connection: Connection
    cursor: Cursor

    def __init__(self):
        self.connection = connect("tasks-tracker.db")
        self.cursor = self.connection.cursor()
        self.prepare_data()

    def prepare_data(self) -> bool:
        create_table_query = """CREATE TABLE IF NOT EXISTS tasks (
                    id text,
                    title text,
                    status text,
                    priority text,
                    description text,
                    start_date text,
                    end_date text
                    )"""
        try:
            with self.connection:
                self.connection.cursor().execute(create_table_query)
            return True
        except Exception:
            print_error(error_message=DATA_CONNECTION_ERROR, with_trace=True)
            return False

    def add_new_task(self, task: Task) -> bool:
        insert_task_query = """INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)"""

        try:
            with self.connection:
                self.connection.cursor().execute(
                    insert_task_query,
                    (
                        task.id,
                        task.title,
                        task.status,
                        task.priority,
                        task.description,
                        task.start_date,
                        task.end_date,
                    ),
                )

            return True
        except Exception:
            print_error(error_message=DATA_CONNECTION_ERROR, with_trace=True)
            return False
