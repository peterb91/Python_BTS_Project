import sqlite3
import datetime
from algorithm import power_management
from input import read_file


class DatabaseArchiver:
    """Creates database and handles inserting data into the database."""
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

    def __init__(self, database_name):
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

    def save_measurement(self, measurements):
        """Saves measurements into the database."""
        values = []
        nrecords = 0
        for measurement in measurements:
            try:
                timestamp = measurement[self.M_TIME_STAMP]
            except IndexError:
                timestamp = datetime.datetime.now()
            nrecords += 1
            values.extend([measurement[self.M_DIRECTION], measurement[self.M_CELL],
                           measurement[self.M_MOBILE_STATION], measurement[self.M_SIGNAL_STRENGTH],
                           measurement[self.M_SIGNAL_QUALITY], timestamp])
            if nrecords > 30:
                self.connection.execute(
                    '''INSERT INTO measurements(direction, cell, mobile_station,
                        signal_strength, signal_quality, time_stamp) VALUES {}'''.format(
                        ', '.join(['(?, ?, ?, ?, ?, ?)'] * nrecords)),
                    values
                )
                values.clear()
                nrecords = 0
        if nrecords > 0:
            self.connection.execute(
                '''INSERT INTO measurements(direction, cell, mobile_station,
                    signal_strength, signal_quality, time_stamp) VALUES {}'''.format(
                    ', '.join(['(?, ?, ?, ?, ?, ?)'] * nrecords)),
                values
            )
        self.connection.commit()

    def save_response(self, responses):
        """Saves calculated response into the database."""
        for response in responses:
            print(response)
            if len(response) > 4:
                try:
                    timestamp = response[self.R_TIME_STAMP]
                except IndexError:
                    timestamp = datetime.datetime.now()
                self.connection.execute(
                    '''INSERT INTO responses(direction, cell, mobile_station,
                        command, step, time_stamp) VALUES (?, ?, ?, ?, ?, ?);''',
                    (response[self.R_DIRECTION], response[self.R_CELL],
                     response[self.R_MOBILE_STATION], response[self.R_COMMAND],
                     response[self.R_STEP], timestamp
                     )
                )
        self.connection.commit()

archiver = DatabaseArchiver('/tmp/BTS.db')
archiver.save_response(power_management())
archiver.save_measurement(read_file())
