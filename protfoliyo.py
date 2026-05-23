from flask import Flask, render_template, jsonify, request
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

portfolio_data = {
    "name": "Sumit Jethva",
    "role": "Data Scientist",
    "tagline": "Turning raw data into meaningful decisions.",
    "about": (
        "I'm a passionate Data Scientist with a strong background in machine learning, "
        "statistical analysis, and data visualization. I love uncovering hidden patterns "
        "in complex datasets and building models that drive real-world impact. "
        "From exploratory analysis to deploying production-grade ML pipelines, "
        "I bring clarity to complexity."
    ),
    "email": "sumit.jethva@email.com",
    "linkedin": "https://linkedin.com/in/sumitjethva",
    "github": "https://github.com/sumitjethva",
    "location": "Bhavnagar, Gujarat, India",
    "skills": {
        "Languages & Libraries": [
            {"name": "Python", "level": 95},
            {"name": "SQL", "level": 75},
            {"name": "MySQL", "level": 88},
            {"name": "NumPy / Pandas", "level": 93},
            {"name": "Scikit-learn", "level": 90},
        ],
        "Machine Learning": [
            {"name": "Regression & Classification", "level": 92},
            {"name": "Deep Learning (PyTorch)", "level": 82},
            {"name": "NLP", "level": 80},
            {"name": "Time Series Forecasting", "level": 85},
            {"name": "Feature Engineering", "level": 90},
        ],
        "Tools & Platforms": [
            {"name": "Jupyter / VS Code", "level": 95},
            {"name": "Tableau / Power BI", "level": 78},
            {"name": "Git & GitHub", "level": 88},
            {"name": "AWS / GCP (basics)", "level": 72},
            {"name": "Docker", "level": 70},
        ],
    },
    "projects": [
        {
            "title": "Customer Churn Prediction",
            "description": (
                "Built an end-to-end churn prediction pipeline using XGBoost and SHAP values "
                "for interpretability. Achieved 94% AUC on telecom data, helping the business "
                "reduce churn by 18%."
            ),
            "tech": ["Python", "XGBoost", "SHAP", "Pandas", "Flask"],
            "github": "https://github.com/sumitjethva/churn-prediction",
        },
        {
            "title": "Sales Forecasting Dashboard",
            "description": (
                "Developed a time-series forecasting model using Facebook Prophet and visualized "
                "results in an interactive Tableau dashboard. Forecasted monthly revenue with "
                "MAPE under 5%."
            ),
            "tech": ["Python", "Prophet", "Tableau", "SQL"],
            "github": "https://github.com/sumitjethva/sales-forecast",
        },
        {
            "title": "Sentiment Analysis — Product Reviews",
            "description": (
                "Fine-tuned a BERT-based model on 50K Amazon product reviews for multi-class "
                "sentiment classification. Deployed as a REST API with FastAPI, achieving 89% F1 score."
            ),
            "tech": ["Python", "HuggingFace", "FastAPI", "PyTorch", "Docker"],
            "github": "https://github.com/sumitjethva/sentiment-api",
        },
        {
            "title": "COVID-19 Data Explorer",
            "description": (
                "Interactive data exploration tool built with Plotly Dash to visualize global "
                "COVID-19 trends. Integrated live data feeds and geospatial heatmaps for 180+ countries."
            ),
            "tech": ["Python", "Plotly Dash", "Pandas", "GeoPandas"],
            "github": "https://github.com/sumitjethva/covid-explorer",
        },
    ],
    "education": [
        {
            "degree": "B.Tech in Computer Science & Engineering",
            "institute": "Dharmsinh Desai University",
            "location": "Nadiad, Gujarat",
            "year": "2019 – 2023",
            "details": "Specialization in Data Science & AI. CGPA: 8.7 / 10.",
        },
        {
            "degree": "Data Science Specialization (Online)",
            "institute": "Coursera — Johns Hopkins University",
            "location": "Online",
            "year": "2023",
            "details": "10-course specialization covering R, statistics, ML, and capstone project.",
        },
    ],
}


@app.route("/")
def index():
    return render_template("index.html", data=portfolio_data)


@app.route("/api/portfolio")
def api_portfolio():
    return jsonify(portfolio_data)


# ─── Email Config ──────────────────────────────────────────────────────────────
# Set these as environment variables or replace directly (not recommended in prod)
EMAIL_SENDER   = "your_gmail@gmail.com"  # Gmail you send FROM
EMAIL_PASSWORD = "cekkekmtkiudhaog"    # Gmail App Password
EMAIL_RECEIVER = "sumit.jethva@gmail.com" # Your inbox


@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    name    = data.get("name", "").strip()
    email   = data.get("email", "").strip()
    subject = data.get("subject", "").strip()
    message = data.get("message", "").strip()

    if not all([name, email, subject, message]):
        return jsonify({"success": False, "error": "All fields are required."}), 400

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Portfolio Contact: {subject}"
        msg["From"]    = EMAIL_SENDER
        msg["To"]      = EMAIL_RECEIVER
        msg["Reply-To"] = email

        html_body = f"""
        <html><body style="font-family:Inter,sans-serif;color:#0f172a;max-width:600px;margin:auto;padding:24px">
          <div style="background:#3b82f6;border-radius:12px 12px 0 0;padding:20px 28px">
            <h2 style="color:#fff;margin:0">📬 New Portfolio Message</h2>
          </div>
          <div style="border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;padding:28px">
            <p><strong>From:</strong> {name} &lt;{email}&gt;</p>
            <p><strong>Subject:</strong> {subject}</p>
            <hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0"/>
            <p style="white-space:pre-wrap;color:#334155">{message}</p>
            <hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0"/>
            <p style="font-size:.8rem;color:#94a3b8">Sent from your portfolio contact form.</p>
          </div>
        </body></html>
        """

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        return jsonify({"success": True, "message": "Message sent successfully!"})

    except smtplib.SMTPAuthenticationError:
        return jsonify({"success": False, "error": "Email authentication failed. Check your App Password."}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)