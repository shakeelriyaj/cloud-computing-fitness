import json
import random
from datetime import datetime, timedelta

exercises = ["squat", "bench_press", "deadlift", "bicep_curl", "shoulder_press"]

def make_session(i):
    exercise = random.choice(exercises)
    reps = random.randint(6, 12)

    start_velocity = round(random.uniform(0.45, 0.75), 2)
    velocity_drop = round(random.uniform(0.1, 0.25), 2)

    velocity = []
    for r in range(reps):
        val = start_velocity - (velocity_drop * (r / max(reps - 1, 1))) + random.uniform(-0.02, 0.02)
        velocity.append(round(max(0.2, val), 2))

    accel_data = [round(random.uniform(1.0, 2.0), 2) for _ in range(reps)]
    heart_rate = random.randint(120, 170)

    return {
        "user_id": f"user_{i:03}",
        "exercise": exercise,
        "accel_data": accel_data,
        "velocity": velocity,
        "heart_rate": heart_rate,
        "duration_sec": random.randint(30, 75),
        "timestamp": (datetime.now() - timedelta(minutes=i*5)).isoformat()
    }

data = [make_session(i) for i in range(1, 21)]

with open("sample_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Generated sample_data.json")