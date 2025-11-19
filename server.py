# server.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
import os

# ---------------- CONFIG ----------------
API_KEY = "some_secret_key_here"   # must match frontend
EMAIL_ADDRESS = "sahilrajpatel90@gmail.com"      # <-- put your email
EMAIL_PASSWORD = "uzru mvqx cxlb jupc"           # <-- Gmail App Password
PORT = int(os.getenv("PORT", 5000))
# ----------------------------------------

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # allow all origins

# ---------------- EMAIL FUNCTION ----------------
def send_email(receiver, subject, body):
    try:
        msg = MIMEText(body)
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver
        msg["Subject"] = subject

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver, msg.as_string())
        server.quit()
        return True, None
    except Exception as e:
        print("Email error:", e)
        return False, str(e)

# ---------------- ROUTES ----------------
@app.route("/sahil", methods=["GET"])
def home():
    return "Flask Email Server Running"

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"ok": True, "message": "API reachable"})

@app.route("/")
def sahil_page():  # unique function name
    return render_template("index.html")

@app.route("/send_alert_email", methods=["POST"])
def send_alert_email():
    # API key check
    header_key = request.headers.get("x-api-key", "")
    if API_KEY and header_key != API_KEY:
        return jsonify({"ok": False, "error": "Invalid API key"}), 401

    data = request.get_json(force=True)
    if not data:
        return jsonify({"ok": False, "error": "Invalid JSON"}), 400

    to = data.get("to")
    subject = data.get("subject")
    body = data.get("body")

    if not to or not subject or not body:
        return jsonify({"ok": False, "error": "Missing fields: 'to'/'subject'/'body' required"}), 400

    ok, err = send_email(to, subject, body)
    if ok:
        return jsonify({"ok": True, "message": "Email sent"})
    else:
        return jsonify({"ok": False, "error": err}), 500

if __name__ == "__main__":
    print(f"Starting Flask server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
