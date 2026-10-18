pipeline {
    agent any
    options { timestamps() }
    environment {
        STUDENT_NAME = 'Daulet'
        STUDENT_SURNAME = 'Bazarali'
        STUDENT_GROUP = 'IT2-2308'
        STUDENT_ID = '37392'
        IMAGE_NAME = 'bazarali-daulet-devops'
        CONTAINER_NAME = 'bazarali-daulet-container'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }
        stage('Build') {
            steps { sh 'python3 -m compileall -q app' }
        }
        stage('Test') {
            steps { sh 'python3 -m unittest discover -s tests -v' }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t "$IMAGE_NAME" .' }
        }
        stage('Docker Run') {
            steps {
                sh '''
                    set -eu
                    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
                    docker run -d \
                      --name "$CONTAINER_NAME" \
                      -p 8085:8080 \
                      -e STUDENT_NAME="$STUDENT_NAME" \
                      -e STUDENT_SURNAME="$STUDENT_SURNAME" \
                      -e STUDENT_GROUP="$STUDENT_GROUP" \
                      -e STUDENT_ID="$STUDENT_ID" \
                      "$IMAGE_NAME"
                    python3 - <<'PY'
import time
import urllib.request
url = 'http://127.0.0.1:8085/health'
for attempt in range(30):
    try:
        with urllib.request.urlopen(url, timeout=2) as r:
            if r.status == 200:
                print('HTTP HEALTH CHECK: SUCCESS')
                break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit('Container health check FAILED')
PY
                    docker ps -a --filter "name=$CONTAINER_NAME"
                    docker logs "$CONTAINER_NAME"
                '''
            }
        }
    }
    post {
        success {
            echo "Student: ${env.STUDENT_NAME} ${env.STUDENT_SURNAME}"
            echo "Group: ${env.STUDENT_GROUP}"
            echo "Student ID: ${env.STUDENT_ID}"
            echo 'Finished stages successfully. Jenkins should report: Finished: SUCCESS'
        }
    }
}
