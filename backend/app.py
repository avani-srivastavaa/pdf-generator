from flask import Flask, request, send_file, jsonify, session, render_template
from flask_cors import CORS
import uuid
import psycopg2
from auth import check_login
from utils import render_pdf
from db import get_certificate_by_uid  
from db import get_connection
import os
from dateutil.relativedelta import relativedelta
from datetime import datetime
from config import Config
import traceback

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, supports_credentials=True, origins=[
    "http://localhost:3000", 
    "https://pdf-generator-frontend.onrender.com"
    ])
@app.route('/')
def home():
    return "PDF Generator backend is running!"

@app.route("/debug-db-url")
def debug_db_url():
    return jsonify({"DATABASE_URL": os.getenv("DATABASE_URL")})

@app.route('/healthz')
def health_check():
    return "OK", 200

@app.route('/api/health')
def api_health():
    return jsonify({"status": "ok"}), 200


@app.route('/test')
def test():
    return jsonify({"status": "ok"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print("== LOGIN DATA RECEIVED ==", data)
    if check_login(data['username'], data['password']):
        return jsonify({"token": "securetoken123"})  # Simple static token
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/generate', methods=['POST'])
def generate():
    try:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "")

        if token != "securetoken123":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.json
        print("== RECEIVED DATA ==\n", data)
        uid = str(uuid.uuid4())
        data['uid'] = uid

        from_date = datetime.strptime(data['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(data['to_date'], '%Y-%m-%d')
        delta = relativedelta(to_date, from_date)

        duration_parts = []
        if delta.years:
            duration_parts.append(f"{delta.years} year{'s' if delta.years > 1 else ''}")
        if delta.months:
            duration_parts.append(f"{delta.months} month{'s' if delta.months > 1 else ''}")
        if delta.days:
            duration_parts.append(f"{delta.days} day{'s' if delta.days > 1 else ''}")
        data['duration'] = ", ".join(duration_parts) or " "

        # Save to DB
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO certificates (from_date, to_date, uid, name, position, role, type, date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (data['from_date'],data['to_date'],uid,data['name'],data['position'],data['role'],data['type'],data['date']))
        conn.commit()
        cur.close()
        conn.close()

        # Render PDF using your actual function
        pdf_path = render_pdf(data)
        print("== PDF GENERATED AT ==\n", pdf_path)

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print("== ERROR OCCURRED IN /generate ==")
        traceback.print_exc()  # <== Shows full stack trace
        return jsonify({"error": str(e)}), 500

def format_date(value):
    return value.strftime("%Y-%m-%d") if hasattr(value, "strftime") else value

@app.route('/verify', methods=['GET'])
def verify_certificate():
    uid = request.args.get('uid')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM certificates WHERE uid = %s", (uid,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        data = {
            "uid": result[0],
            "name": result[1],
            "position": result[2],
            "role": result[3],
            "type": result[4],
            "from_date": format_date(result[5]),
            "to_date": format_date(result[6]),
            "date": format_date(result[7])
            }
        return render_template("verified.html", data=data)
    else:
        return "Certificate not found", 404


@app.route('/session')
def check_session():
    return jsonify({"logged_in": session.get("logged_in", False)})

if __name__ == '__main__':
    app.run(debug=True)
