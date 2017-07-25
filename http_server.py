from database import DatabaseArchiver
from flask import Flask, request


app = Flask(__name__)
DATABASE_NAME = '/tmp/BTS-http.db'


@app.route('/measurements', methods=['POST'])
def populate_measurements():
    data = request.get_json()
    archiver = DatabaseArchiver(DATABASE_NAME)
    for element in data:
        archiver.save_measurement([
            element['direction'],
            element['cell'],
            element['station'],
            element['signal_strength'],
            element['signal_quality'],
            element['timestamp']
        ])
    archiver.flush()
    return 'OK'


@app.route('/responses', methods=['POST'])
def populate_responses():
    data = request.get_json()
    archiver = DatabaseArchiver(DATABASE_NAME)
    for element in data:
        archiver.save_response([
            element['direction'],
            element['cell'],
            element['station'],
            element['command'],
            element['step'],
            element['timestamp']
        ])
    archiver.flush()
    return 'OK'

if __name__ == '__main__':
    app.run()
