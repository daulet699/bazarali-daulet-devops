# DevOps individual lab: Linux -> Git -> GitHub -> Docker -> Jenkins

This repository contains a **personalized student web application** created for the DevOps individual laboratory task. The application uses Python standard library and supports Docker environment variables.

## Run and test

```bash
python3 -m unittest discover -s tests -v
python3 -m app.main
# In another terminal:
curl http://localhost:8080/
curl http://localhost:8080/health
```

## Docker

```bash
docker build -t bazarali-daulet-devops .
docker run -d --name bazarali-daulet-container -p 8085:8080 bazarali-daulet-devops
curl http://localhost:8085/
docker logs bazarali-daulet-container
docker ps -a
# Stop/remove before using Docker Compose:
docker stop bazarali-daulet-container
docker rm bazarali-daulet-container
docker compose up -d --build
curl http://localhost:8085/health
docker compose down
```

## Jenkins

Create a Pipeline job `Bazarali_Daulet_DevOps` and choose **Pipeline script from SCM**, Git repository URL, branch `*/main`, script path `Jenkinsfile`. The Jenkins executor must have `git`, `python3`, `docker` and permission to access Docker daemon. Port 8085 must be free.

Student: Daulet Bazarali / IT2-2308 / 37392

## Health Check
GET /health checks application availability.
