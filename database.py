import sqlite3
import datetime
import requests


class BaseArchiver():
    """Base class for database saving"""

    M_DIRECTION = 0
    M_CELL = 1
    M_MOBILE_STATION = 2
    M_SIGNAL_STRENGTH = 3
    M_SIGNAL_QUALITY = 4
    M_TIME_STAMP = 5
    R_DIRECTION = 0
    R_CELL = 1
    R_MOBILE_STATION = 2
    R_COMMAND = 3
    R_STEP = 4
    R_TIME_STAMP = 5

    def __init__(self):
        self.measurements_buffer = []
        self.responses_buffer = []
        self.measurements_buffer_limit = 100
        self.responses_buffer_limit = 100

    def save_measurement(self, data):
        """Saves a single measurement."""
        record = list(data)
        try:
            timestamp = record[self.M_TIME_STAMP]
        except IndexError:
            timestamp = datetime.datetime.now()
            record.append(timestamp)
        self.measurements_buffer.append(record)
        if len(self.measurements_buffer) > self.measurements_buffer_limit:
            self.flush_measurements()

    def save_response(self, response):
        """Saves a single response."""
        if len(response) < 5:
            return
        record = list(response)
        try:
            timestamp = record[self.R_TIME_STAMP]
        except IndexError:
            timestamp = datetime.datetime.now()
            record.append(timestamp)
        self.responses_buffer.append(record)
        if len(self.responses_buffer) > self.measurements_buffer_limit:
            self.flush_responses()

    def flush(self):
        """If there is buffering involved, flush any remaining records."""
        self.flush_measurements()
        self.flush_responses()


class DatabaseArchiver(BaseArchiver):
    """Creates database and handles inserting data into the database."""

    def __init__(self, database_name):
        super().__init__()
        self.connection = sqlite3.connect(database_name)
        self.create_schema()

    def create_schema(self):
        """Creates schema if not created before."""
        if self.create_schema_needed():
            c = self.connection.cursor()
            c.execute(
                '''CREATE TABLE measurements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        direction TEXT,
                        cell TEXT,
                        mobile_station TEXT,
                        signal_strength REAL,
                        signal_quality INTEGER,
                        time_stamp DATETIME
                        );'''
            )
            c.execute(
                '''CREATE TABLE responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        direction TEXT,
                        cell TEXT,
                        mobile_station TEXT,
                        command TEXT,
                        step INTEGER,
                        time_stamp DATETIME
                        );'''
            )
            self.connection.commit()

    def create_schema_needed(self):
        """Checks if the schema already exists."""
        c = self.connection.cursor()
        try:
            c.execute('''SELECT * FROM measurements LIMIT 1;''')
        except sqlite3.OperationalError:
            return True
        return False

    def flush_measurements(self):
        """Performs actual database insert for measurements"""
        ins_buffer = []
        values_buffer = []
        for item in self.measurements_buffer:
            ins_buffer.append('(?, ?, ?, ?, ?, ?)')
            values_buffer.extend([
                item[self.M_DIRECTION], item[self.M_CELL],
                item[self.M_MOBILE_STATION], item[self.M_SIGNAL_STRENGTH],
                item[self.M_SIGNAL_QUALITY], item[self.M_TIME_STAMP]
            ])
        if len(ins_buffer) == 0:
            return
        sql = '''INSERT INTO measurements (
                direction, cell, mobile_station, signal_strength, signal_quality, time_stamp
                ) VALUES {}'''.format(', '.join(ins_buffer))
        self.connection.execute(sql, values_buffer)
        self.connection.commit()
        self.measurements_buffer.clear()

    def flush_responses(self):
        """Performs actual database insert for responses"""
        ins_buffer = []
        values_buffer = []
        for item in self.responses_buffer:
            ins_buffer.append('(?, ?, ?, ?, ?, ?)')
            values_buffer.extend([
                item[self.R_DIRECTION], item[self.R_CELL],
                item[self.R_MOBILE_STATION], item[self.R_COMMAND],
                item[self.R_STEP], item[self.R_TIME_STAMP]
            ])
        if len(ins_buffer) == 0:
            return
        sql = '''INSERT INTO responses (
                   direction, cell, mobile_station, command, step, time_stamp
                   ) VALUES {}'''.format(', '.join(ins_buffer))
        self.connection.execute(sql, values_buffer)
        self.connection.commit()
        self.responses_buffer.clear()


class HTTPArchiver(BaseArchiver):
    """Sends input and calculated output to the database via HTTP server"""

    ROUTE_SAVE_MEASUREMENTS = '/measurements'
    ROUTE_SAVE_RESPONSES = '/responses'

    def __init__(self, baseurl):
        super().__init__()
        self.baseurl = baseurl
        self.session = requests.session()

    def flush_measurements(self):
        url = ''.join([self.baseurl, self.ROUTE_SAVE_MEASUREMENTS])
        data = [
            {
                'timestamp': measurement[self.M_TIME_STAMP].isoformat(' '),
                'direction': measurement[self.M_DIRECTION],
                'cell': measurement[self.M_CELL],
                'station': measurement[self.M_MOBILE_STATION],
                'signal_strength': measurement[self.M_SIGNAL_STRENGTH],
                'signal_quality': measurement[self.M_SIGNAL_QUALITY],
            }
            for measurement in self.measurements_buffer
        ]
        self.session.post(url, json=data)
        self.measurements_buffer.clear()

    def flush_responses(self):
        url = ''.join([self.baseurl, self.ROUTE_SAVE_RESPONSES])
        data = [
            {
                'timestamp': response[self.R_TIME_STAMP].isoformat(' '),
                'step': response[self.R_STEP],
                'command': response[self.R_COMMAND],
                'station': response[self.R_MOBILE_STATION],
                'cell': response[self.R_CELL],
                'direction': response[self.R_DIRECTION]
            }
            for response in self.responses_buffer
        ]
        self.session.post(url, json=data)
        self.responses_buffer.clear()
