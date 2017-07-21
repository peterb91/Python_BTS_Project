import sqlite3
import datetime


class DatabaseArchiver:
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
        c = self.connection.cursor()
        try:
            c.execute('''SELECT * FROM measurements LIMIT 1;''')
        except sqlite3.OperationalError:
            return True
        return False

    def save_measurement(self, measurement):
        try:
            timestamp = measurement[self.M_TIME_STAMP]
        except IndexError:
            timestamp = datetime.datetime.now()
        c = self.connection.cursor()
        c.execute(
            '''INSERT INTO measurements(direction, cell, mobile_station,
                signal_strength, signal_quality, time_stamp) VALUES (?, ?, ?, ?, ?, ?);''',
            (measurement[self.M_DIRECTION], measurement[self.M_CELL],
             measurement[self.M_MOBILE_STATION], measurement[self.M_SIGNAL_STRENGTH],
             measurement[self.M_SIGNAL_QUALITY], timestamp
             )
        )
        self.connection.commit()

    def save_response(self, response):
        try:
            timestamp = response[self.R_TIME_STAMP]
        except IndexError:
            timestamp = datetime.datetime.now()
        c = self.connection.cursor()
        c.execute(
            '''INSERT INTO measurements(direction, cell, mobile_station,
                command, step, time_stamp) VALUES (?, ?, ?, ?, ?, ?);''',
            (response[self.R_DIRECTION], response[self.R_CELL],
             response[self.R_MOBILE_STATION], response[self.R_COMMAND],
             response[self.R_STEP], timestamp
             )
        )
        self.connection.commit()

# archiver = DatabaseArchiver('/tmp/DB.db')
#
# data = [
#     ['DL', 'S0', 'MS776', -66, 1],
#     ['DL', 'S0', 'MS222', -76, 2],
#     ['UL', 'S0', 'MS776', -78, 2],
#     ['DL', 'S0', 'MS776', -63, 1],
#     ['DL', 'S0', 'MS222', -73, 1],
#     ['DL', 'N1', 'MS776', -79, None],
#     ['DL', 'N2', 'MS776', -88, None],
#     ['DL', 'N1', 'MS222', -91, None],
#     ['DL', 'N3', 'MS222', -92, None],
#     ['UL', 'S0', 'MS776', -75, 2],
#     ['DL', 'S0', 'MS776', -60, 0],
#     ['DL', 'S0', 'MS222', -77, 2],
#     ['DL', 'N1', 'MS776', -89, None],
#     ['DL', 'N2', 'MS776', -92, None],
#     ['UL', 'S0', 'MS776', -70, 1],
#     ['DL', 'N1', 'MS222', -94, None],
#     ['DL', 'N3', 'MS222', -93, None],
#     ['DL', 'S0', 'MS776', -61, 0],save_measurement
#     ['UL', 'S0', 'MS776', -70, 1]
# ]
#
# for d in data:
#     archiver.save_measurement(d)
