from flask import Flask, request, jsonify
import math
import statistics

app = Flask(__name__)

def magnitude(x, y, z):
    return math.sqrt(x * x + y * y + z * z)

def count_peaks(values, threshold):
    peaks = 0
    for i in range(1, len(values) - 1):
        if values[i] > values[i - 1] and values[i] > values[i + 1] and values[i] > threshold:
            peaks += 1
    return peaks

def safe_mean(values):
    return sum(values) / len(values) if values else 0

@app.route("/", methods=["GET"])
def home():
    return {"message": "Fitness analytics service is running"}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(force=True)

    user_id = data.get("user_id", "unknown")
    session_id = data.get("session_id", "unknown")
    exercise = data.get("exercise", "unknown")
    sent_at = data.get("sent_at", None)
    samples = data.get("samples", [])

    if not samples:
        return jsonify({"error": "samples array is required"}), 400

    accel_mags = []
    gyro_mags = []
    timestamps = []

    for s in samples:
        ax = float(s.get("ax", 0))
        ay = float(s.get("ay", 0))
        az = float(s.get("az", 0))
        gx = float(s.get("gx", 0))
        gy = float(s.get("gy", 0))
        gz = float(s.get("gz", 0))
        t = float(s.get("t", 0))

        accel_mags.append(magnitude(ax, ay, az))
        gyro_mags.append(magnitude(gx, gy, gz))
        timestamps.append(t)

    avg_accel = safe_mean(accel_mags)
    avg_gyro = safe_mean(gyro_mags)
    max_accel = max(accel_mags) if accel_mags else 0
    max_gyro = max(gyro_mags) if gyro_mags else 0

    accel_std = statistics.pstdev(accel_mags) if len(accel_mags) > 1 else 0
    gyro_std = statistics.pstdev(gyro_mags) if len(gyro_mags) > 1 else 0

    peak_threshold = avg_accel + 0.3 * accel_std
    rep_count = count_peaks(accel_mags, peak_threshold)

    first_half = accel_mags[: max(1, len(accel_mags) // 2)]
    second_half = accel_mags[len(accel_mags) // 2 :]

    first_half_avg = safe_mean(first_half)
    second_half_avg = safe_mean(second_half)

    fatigue_score = max(0, first_half_avg - second_half_avg)

    consistency_penalty = accel_std * 8
    form_score = max(0, min(100, int(100 - consistency_penalty)))

    if fatigue_score > 0.15:
        recommendation = "Fatigue rising - consider reducing load or resting longer"
    elif form_score < 75:
        recommendation = "Movement consistency is low - focus on form"
    else:
        recommendation = "Set looks consistent - maintain current plan"

    return jsonify({
        "user_id": user_id,
        "session_id": session_id,
        "exercise": exercise,
        "sent_at": sent_at,
        "sample_count": len(samples),
        "rep_count_estimate": rep_count,
        "avg_accel_magnitude_g": round(avg_accel, 4),
        "avg_gyro_magnitude_dps": round(avg_gyro, 4),
        "max_accel_magnitude_g": round(max_accel, 4),
        "max_gyro_magnitude_dps": round(max_gyro, 4),
        "fatigue_score": round(fatigue_score, 4),
        "form_score": form_score,
        "recommendation": recommendation
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)