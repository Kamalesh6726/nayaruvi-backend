from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Email credentials (use Gmail App Password)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

if not EMAIL_USER or not EMAIL_PASS:
    raise RuntimeError("❌ EMAIL_USER or EMAIL_PASS not set in .env file")

# -------------------------------
# Registration Email
# -------------------------------
@app.route("/send-email", methods=["POST"])
def send_email():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    pincode = data.get("pincode")

    if not all([name, email, pincode]):
        return jsonify({"success": False, "error": "Missing fields"}), 400

    try:
        msg = EmailMessage()
        msg["Subject"] = "Nayaruvi – Air Quality Alert Registration Successful"
        msg["From"] = EMAIL_USER
        msg["To"] = email

        msg.set_content(f"""
Dear {name},

✅ You have been successfully registered for Nayaruvi Air Quality Alerts.

📍 Registered PIN Code: {pincode}

You will now receive email alerts whenever air quality in your area becomes unsafe.

🌱 Stay informed. Stay safe.

Regards,
Team Nayaruvi
Government of India – Environmental Intelligence Platform
        """)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return jsonify({"success": True, "message": "Registration email sent"})

    except Exception as e:
        print("Email Error:", e)
        return jsonify({"success": False, "error": "Email sending failed"}), 500


# -------------------------------
# Send Current AQI Status Email
# -------------------------------
@app.route("/send-aqi-status", methods=["POST"])
def send_aqi_status():
    data = request.get_json()

    email = data.get("email")
    location = data.get("location")
    aqi = data.get("aqi")
    status = data.get("status")
    advice = data.get("advice")

    if not all([email, location, aqi, status, advice]):
        return jsonify({"success": False, "error": "Missing AQI data"}), 400

    try:
        msg = EmailMessage()
        msg["Subject"] = "Nayaruvi – Live Air Quality Status Update"
        msg["From"] = EMAIL_USER
        msg["To"] = email

        msg.set_content(f"""
Dear Citizen,

🌍 Nayaruvi – Real-Time Air Quality Update

📍 Location : {location}
📊 AQI Value : {aqi}
⚠ AQI Status: {status}

🛡 Health Advisory:
{advice}

Please follow the recommended safety measures.

Regards,
Team Nayaruvi
Government of India – Environmental Intelligence Platform
        """)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return jsonify({"success": True, "message": "AQI email sent successfully"})

    except Exception as e:
        print("AQI Email Error:", e)
        return jsonify({"success": False, "error": "AQI email sending failed"}), 500


# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

