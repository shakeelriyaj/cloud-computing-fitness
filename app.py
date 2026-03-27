from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"message": "Fitness analytics service is running"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    velocity = data.get("velocity", [])
    accel = data.get("accel_data", [])
    heart_rate = data.get("heart_rate", 0)
    exercise = data.get("exercise", "unknown")
    user_id = data.get("user_id", "unknown")

    rep_count = len(velocity)
    avg_velocity = sum(velocity) / len(velocity) if velocity else 0

    fatigue_score = max(0, velocity[0] - velocity[-1]) if len(velocity) >= 2 else 0
    accel_range = max(accel) - min(accel) if accel else 0
    form_score = max(0, 100 - int(accel_range * 10))

    if fatigue_score > 0.2:
        recommendation = "Reduce weight slightly next set"
    elif avg_velocity < 0.35:
        recommendation = "Focus on explosive movement"
    else:
        recommendation = "Good set, maintain current load"

    return jsonify({
        "user_id": user_id,
        "exercise": exercise,
        "rep_count": rep_count,
        "avg_velocity": round(avg_velocity, 3),
        "fatigue_score": round(fatigue_score, 3),
        "form_score": form_score,
        "heart_rate": heart_rate,
        "recommendation": recommendation
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)