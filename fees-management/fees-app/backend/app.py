from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "fees.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            fee_type TEXT NOT NULL,
            payment_date TEXT NOT NULL,
            payment_mode TEXT NOT NULL,
            status TEXT DEFAULT 'Paid',
            remarks TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized!")

# ─── STUDENTS ───────────────────────────────────────────────

@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db()
    students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(s) for s in students])

@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    try:
        conn = get_db()
        conn.execute(
            'INSERT INTO students (name, roll_no, department, year, email, phone) VALUES (?,?,?,?,?,?)',
            (data['name'], data['roll_no'], data['department'], data['year'], data.get('email',''), data.get('phone',''))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Student added successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Roll number already exists!"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    conn = get_db()
    conn.execute('DELETE FROM fees WHERE student_id=?', (sid,))
    conn.execute('DELETE FROM students WHERE id=?', (sid,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted!"})

# ─── FEES ────────────────────────────────────────────────────

@app.route('/fees', methods=['GET'])
def get_fees():
    conn = get_db()
    fees = conn.execute('''
        SELECT f.*, s.name, s.roll_no, s.department
        FROM fees f JOIN students s ON f.student_id = s.id
        ORDER BY f.id DESC
    ''').fetchall()
    conn.close()
    return jsonify([dict(f) for f in fees])

@app.route('/fees', methods=['POST'])
def add_fee():
    data = request.json
    try:
        conn = get_db()
        conn.execute(
            'INSERT INTO fees (student_id, amount, fee_type, payment_date, payment_mode, status, remarks) VALUES (?,?,?,?,?,?,?)',
            (data['student_id'], data['amount'], data['fee_type'], data['payment_date'],
             data['payment_mode'], data.get('status', 'Paid'), data.get('remarks', ''))
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Fee record added!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fees/<int:fid>', methods=['DELETE'])
def delete_fee(fid):
    conn = get_db()
    conn.execute('DELETE FROM fees WHERE id=?', (fid,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Fee record deleted!"})

# ─── DASHBOARD STATS ─────────────────────────────────────────

@app.route('/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    total_students = conn.execute('SELECT COUNT(*) as c FROM students').fetchone()['c']
    total_fees = conn.execute("SELECT COALESCE(SUM(amount),0) as s FROM fees WHERE status='Paid'").fetchone()['s']
    pending_fees = conn.execute("SELECT COALESCE(SUM(amount),0) as s FROM fees WHERE status='Pending'").fetchone()['s']
    total_records = conn.execute('SELECT COUNT(*) as c FROM fees').fetchone()['c']
    conn.close()
    return jsonify({
        "total_students": total_students,
        "total_fees_collected": total_fees,
        "pending_fees": pending_fees,
        "total_records": total_records
    })

@app.route('/students/<int:sid>/fees', methods=['GET'])
def get_student_fees(sid):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id=?', (sid,)).fetchone()
    fees = conn.execute('SELECT * FROM fees WHERE student_id=? ORDER BY id DESC', (sid,)).fetchall()
    conn.close()
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"student": dict(student), "fees": [dict(f) for f in fees]})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
