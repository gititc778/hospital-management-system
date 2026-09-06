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


# Create patients table if it doesn't exist
with get_db_connection() as conn:
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            age INT
        )
    """)

    conn.commit()


# Get all patients
@app.route('/patients', methods=['GET'])
def get_patients():

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM patients")

        patients = cursor.fetchall()

    return jsonify(patients)


# Add a patient
@app.route('/patients', methods=['POST'])
def add_patient():

    data = request.json

    name = data.get('name')
    age = data.get('age')

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO patients (name, age) VALUES (%s, %s)",
            (name, age)
        )

        conn.commit()

        patient_id = cursor.lastrowid

    return jsonify({
        'id': patient_id,
        'name': name,
        'age': age
    })


# Start Flask application
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=3000
    )