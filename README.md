# cloud-computing-fitness

Okay so basically, i have a docker file adn then i push this to GCP
image registry. here i then grab it from the GCP cloud run function
then this gives us a public URL to hit and get data


docker build -t fitness-analytics-gcp .

docker run -p 8080:8080 fitness-analytics-gcp

docker tag fitness-analytics-gcp us-central1-docker.pkg.dev/fitness-analytics-gcp/fitness-repo/fitness-analytics-gcp

docker push us-central1-docker.pkg.dev/fitness-analytics-gcp/fitness-repo/fitness-analytics-gcp

gcloud run services add-iam-policy-binding fitness-analytics-service1 \
  --member="allUsers" \
  --role="roles/run.invoker" \
  --region=us-central1

https://fitness-analytics-service1-550653652814.us-central1.run.app

curl -X POST "https://fitness-analytics-service1-550653652814.us-central1.run.app/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "exercise": "squat",
    "accel_data": [1.2, 1.5, 1.4, 1.8, 1.6, 1.3],
    "velocity": [0.62, 0.59, 0.55, 0.49, 0.44, 0.39],
    "heart_rate": 152
  }'

  
gcloud auth login
gcloud config set project fitness-analytics-gcp
gcloud auth configure-docker us-central1-docker.pkg.dev