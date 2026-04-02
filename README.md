# cloud-computing-fitness

Okay so basically, i have a docker file adn then i push this to GCP
image registry. here i then grab it from the GCP cloud run function
then this gives us a public URL to hit and get data


docker build -t fitness-analytics-gcp .

docker tag fitness-analytics-gcp us-central1-docker.pkg.dev/fitness-analytics-gcp/fitness-repo/fitness-analytics-gcp

docker push us-central1-docker.pkg.dev/fitness-analytics-gcp/fitness-repo/fitness-analytics-gcp

gcloud run services add-iam-policy-binding fitness-analytics-service \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=us-central1


https://fitness-analytics-service-550653652814.us-central1.run.app


curl -X POST "https://fitness-analytics-service-550653652814.us-central1.run.app/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "session_id": "sess_001",
    "exercise": "squat",
    "sent_at": "2026-04-02T14:30:00Z",
    "samples": [
      {"t": 0.00, "ax": 0.12, "ay": 0.98, "az": 0.04, "gx": 12.4, "gy": 3.1, "gz": 1.7},
      {"t": 0.02, "ax": 0.18, "ay": 1.10, "az": 0.06, "gx": 15.8, "gy": 4.0, "gz": 2.1},
      {"t": 0.04, "ax": 0.42, "ay": 1.35, "az": 0.10, "gx": 22.2, "gy": 5.3, "gz": 2.8},
      {"t": 0.06, "ax": 0.16, "ay": 1.02, "az": 0.05, "gx": 13.1, "gy": 3.2, "gz": 1.9},
      {"t": 0.08, "ax": 0.47, "ay": 1.42, "az": 0.12, "gx": 24.6, "gy": 6.1, "gz": 3.0},
      {"t": 0.10, "ax": 0.14, "ay": 1.01, "az": 0.05, "gx": 12.8, "gy": 3.0, "gz": 1.8}
    ]
  }'


docker run -p 8080:8080 fitness-analytics-gcp

 gcloud run services delete fitness-analytics-gcp --region=us-central1
  
gcloud auth login
gcloud config set project fitness-analytics-gcp
gcloud auth configure-docker us-central1-docker.pkg.dev