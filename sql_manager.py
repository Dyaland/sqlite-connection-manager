import sqlite3


class ConnectionManager:
    """A context manager for sqlite3 connections.
    Example:
    
    with ConnectionManager(database_dict) as cm:
        **run sqlite code**

    data_base-dict format:
    {"database": "filename.db"}
    """

    def __init__(self, *, database: dict, fk: bool = False):
        self.database = database
        self.foreign_keys = fk

    def __enter__(self):
        """Runs when the context opens."""

        self.connection = sqlite3.connect(**self.database)
        self.cursor = self.connection.cursor()  
        self.cursor.execute("BEGIN;")   
        if self.foreign_keys:
            self.cursor.execute('PRAGMA foreign_keys = True;')
        return self

    def __exit__(self, exc_class, exc, traceback):
        """Runs when the context is concluded or an exception is thrown."""

        try:
            # Commit any changes before closing.
            self.connection.commit()
        except AttributeError:
            self.cursor.execute("ROLLBACK;")
            return True  # exception handled successfully
        finally:
            self.connection.close()

    def _execute(self, query: str):
        """Executes the query and returns the result, if any."""

        self.cursor.execute(query)
        return self.cursor.fetchall()


def execute_query(database: dict, query: str):
    """Runs the ConnectionManager as context manager for sql , handling any exceptions and closes connections."""

    with ConnectionManager(database) as cm:
        return (cm._execute(query))
