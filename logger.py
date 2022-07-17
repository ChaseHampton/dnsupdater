import json
import os
import psycopg2

class Logger:
    """Class to handle common logging of dns update checks"""

    def __init__(self):
        self.db_user = os.getenv("DB_USER")
        self.db_pass = os.getenv("DB_PASS")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db = psycopg2.connect(
            host = self.db_host,
            database = "dnsup_logs",
            user = self.db_user,
            password = self.db_pass,
            port = self.db_port
        )

    def log(self, message:str, response:str=""):
        """Standard log function inserts message and response into table"""
        if response:
            self._with_response(message, response)
        else:
            self._without_response(message)        

    def _without_response(self, message):
        script = """INSERT INTO logging (message, log_time) VALUES (%s, now())"""
        with self.db.cursor() as curs:
            curs.execute(script, (message,))
            self.db.commit()

    def _with_response(self, message, response):
        script = """INSERT INTO logging (message, response, log_time) VALUES (%s,%s, now())"""
        with self.db.cursor() as curs:
            curs.execute(script, (message, response))
            self.db.commit()
