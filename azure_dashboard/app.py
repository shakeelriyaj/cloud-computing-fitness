from flask import Flask, render_template_string, request
import requests
import os

app = Flask(__name__)

GCP_ANALYTICS_URL = os.getenv(
    "GCP_ANALYTICS_URL",
    "https://fitness-analytics-gcp-550653652814.us-central1.run.app/analyze"
)

HTML = """
<!doctype html>
<html>
<head>
    <title>Fitness Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        button { padding: 10px 16px; font-size: 16px; }
        pre { background: #f4f4f4; padding: 16px; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Fitness Analytics Dashboard</h1>
    <p>This Azure app sends workout data to the GCP analytics service.</p>
    <form method="post">
        <button type="submit">Run Sample Analysis</button>
    </form>

    {% if result %}
    <h2>Analysis Result</h2>
    <pre>{{ result }}</pre>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        payload = {
            "user_id": "user_001",
            "exercise": "squat",
            "accel_data": [1.2, 1.5, 1.4, 1.8, 1.6, 1.3],
            "velocity": [0.62, 0.59, 0.55, 0.49, 0.44, 0.39],
            "heart_rate": 152
        }

        response = requests.post(GCP_ANALYTICS_URL, json=payload, timeout=30)
        result = response.text

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)