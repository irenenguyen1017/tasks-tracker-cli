from datetime import datetime
from sqlite3 import Connection, Cursor, connect
from typing import List, Optional

from tasks_tracker.configs import DATA_CONNECTION_ERROR, DB_DATE_FORMAT, DB_PATH
from tasks_tracker.model import Task
from tasks_tracker.typing import Priority, Status
from tasks_tracker.utils import print_error


class TasksTrackerData:
    connection: Connection
    cursor: Cursor

    def __init__(self):
        self.connection = connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self.prepare_data()

    def prepare_data(self) -> bool:
        create_table_query = """CREATE TABLE IF NOT EXISTS tasks( id text, title text, status text, priority text, description text, start_date text, end_date text)"""

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

    def get_tasks_list(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Task]:
        print(start_date)

        get_all_tasks_query = """SELECT * from tasks WHERE (status = ?1 OR ?1 IS NULL) AND (priority = ?2 OR ?2 IS NULL) AND (start_date >= ?3 OR ?3 IS NULL) AND (end_date <= ?4 OR ?4 IS NULL OR end_date IS NULL) ORDER BY start_date ASC"""

        try:
            with self.connection:
                self.cursor.execute(
                    get_all_tasks_query,
                    (
                        status.value if status else None,
                        priority.value if priority else None,
                        start_date.strftime(DB_DATE_FORMAT) if start_date else None,
                        end_date.strftime(DB_DATE_FORMAT) if end_date else None,
                    ),
                )
                results = self.cursor.fetchall()
                return [Task(*result) for result in results]

        except Exception:
            print_error(error_message=DATA_CONNECTION_ERROR, with_trace=True)
            return []

    def find_task_by_id(self, id: str) -> Optional[Task]:
        find_task_query = """SELECT * from tasks WHERE id = ?"""

        try:
            with self.connection:
                record = self.cursor.execute(find_task_query, (id,)).fetchone()
                if record:
                    task = Task(*record)
                    return task
                else:
                    return None
        except Exception:
            print_error(error_message=DATA_CONNECTION_ERROR, with_trace=True)
            return None

    def update_task(self, task: Task) -> bool:
        update_query_task = """UPDATE tasks SET title = ?2, status = ?3, priority = ?4, description = ?5, start_date = ?6, end_date = ?7 WHERE id = ?1"""

        try:
            with self.connection:
                self.cursor.execute(
                    update_query_task,
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
