from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb
import MySQLdb.cursors
import os

app = Flask(__name__)
CORS(app)

# MySQL configuration
# Values come from Kubernetes ConfigMap and Secret
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'passwd': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME'),
    'cursorclass': MySQLdb.cursors.DictCursor
}


# Helper function to get DB connection
def get_db_connection():
    return MySQLdb.connect(**DB_CONFIG)


# Liveness probe
# Checks whether the Flask application is running
@app.route('/liveness', methods=['GET'])
def liveness():
    return jsonify({
        'status': 'alive'
    }), 200


# Readiness probe
# Checks whether the application can connect to MySQL
@app.route('/readiness', methods=['GET'])
def readiness():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")

        return jsonify({
            'status': 'ready'
        }), 200

    except Exception:
        return jsonify({
            'status': 'not ready'
        }), 503


# Create appointments table
with get_db_connection() as conn:
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            patient_id INT,
            doctor VARCHAR(255),
            date DATE,
            time TIME
        )
    """)

    conn.commit()


# Get all appointments
@app.route('/appointments', methods=['GET'])
def get_appointments():

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                patient_id,
                doctor,
                DATE_FORMAT(date, '%Y-%m-%d') AS date,
                TIME_FORMAT(time, '%H:%i') AS time
            FROM appointments
        """)

        appointments = cursor.fetchall()

    return jsonify(appointments)


# Add appointment
@app.route('/appointments', methods=['POST'])
def add_appointment():

    data = request.json

    patient_id = data.get('patient_id')
    doctor = data.get('doctor')
    date = data.get('date')
    time = data.get('time')

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO appointments
            (patient_id, doctor, date, time)
            VALUES (%s, %s, %s, %s)
            """,
            (patient_id, doctor, date, time)
        )

        conn.commit()

        appointment_id = cursor.lastrowid

    return jsonify({
        'id': appointment_id,
        'patient_id': patient_id,
        'doctor': doctor,
        'date': date,
        'time': time
    })


# Start Flask application
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=3001
    )