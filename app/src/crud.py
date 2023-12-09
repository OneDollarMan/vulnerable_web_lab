import logging
import psycopg2
from psycopg2.errorcodes import DUPLICATE_TABLE, IN_FAILED_SQL_TRANSACTION
from psycopg2 import errors


class Db:
    def __init__(self, db, user, password, host, port):
        self.connection = psycopg2.connect(database=db, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        try:
            self.cursor.execute("CREATE TABLE notes (id SERIAL PRIMARY KEY, text VARCHAR(64))")
            self.connection.commit()
        except errors.lookup(DUPLICATE_TABLE):
            logging.info('tables created already')
            return True
        logging.info('tables created succesfully')
        return True

    def execute_query_insecure(self, query):
        try:
            self.cursor.execute(query)
        except errors.lookup(IN_FAILED_SQL_TRANSACTION):
            self.connection.rollback()
            return None
        self.connection.commit()

    def execute_query_secure(self, query, params):
        try:
            self.cursor.execute(query, params)
        except errors.lookup(IN_FAILED_SQL_TRANSACTION):
            self.connection.rollback()
            return None
        self.connection.commit()

    def get_query_all_secure(self, query, params=None):
        try:
            if params is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, params)
        except errors.lookup(IN_FAILED_SQL_TRANSACTION):
            self.connection.rollback()
            return None
        return self.cursor.fetchall()

    def add_note_insecure(self, text):
        self.execute_query_insecure(f"INSERT INTO notes(text) VALUES ('{text}');")

    def add_note_secure(self, text):
        self.execute_query_secure("INSERT INTO notes(text) VALUES (%s);", (text, ))

    def get_notes_secure(self):
        return self.get_query_all_secure("SELECT * FROM notes;")

    def get_note_secure(self, id):
        return self.get_query_all_secure("SELECT * FROM notes WHERE id=%s", (id, ))
