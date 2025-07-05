
from flask import Flask, request, send_file, jsonify, session
from flask_cors import CORS
from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from auth import check_login
from utils import render_pdf

app = Flask(__name__)
app.secret_key = 'supersecretkey'


app.config.update(
    SESSION_COOKIE_SAMESITE='None',   # Allow cross-origin session
    SESSION_COOKIE_SECURE=False       # Set to True in production over HTTPS
)

CORS(app, supports_credentials=True, origins=["https://your-frontend.onrender.com"])

@app.route('/login', methods=['POST'])
def login():
    data = request.json
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

        pdf_path = render_pdf(data)
        print("== PDF GENERATED AT ==\n", pdf_path)

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print("== ERROR OCCURRED IN /generate ==\n", e)
        return jsonify({"error": str(e)}), 500



@app.route('/session')
def check_session():
    return jsonify({"logged_in": session.get("logged_in", False)})

if __name__ == '__main__':
    app.run(debug=True)
