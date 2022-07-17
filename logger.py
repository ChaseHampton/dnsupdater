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
            host=self.db_host,
            database="dnsup_logs",
            user=self.db_user,
            password=self.db_pass,
            port=self.db_port,
        )

    def log(
        self, message: str, domain: str, home_ip: str, cf_ip: str, response: str = ""
    ):
        """Standard log function inserts message and response into table"""
        if response:
            self._with_response(domain, home_ip, cf_ip, message, response)
        else:
            self._without_response(domain, home_ip, cf_ip, message)

    def _without_response(self, domain, home_ip, cf_ip, message):
        script = """INSERT INTO logging (domain_name, home_ip, cf_ip, message, log_time) VALUES (%s,%s,%s,%s,now())"""
        with self.db.cursor() as curs:
            curs.execute(script, (domain, home_ip, cf_ip, message))
            self.db.commit()

    def _with_response(self, domain, home_ip, cf_ip, message, response):
        script = """INSERT INTO logging (domain_name, home_ip, cf_ip, message, response, log_time) VALUES (%s,%s,%s,%s,%s,now())"""
        with self.db.cursor() as curs:
            curs.execute(script, (domain, home_ip, cf_ip, message, response))
            self.db.commit()
