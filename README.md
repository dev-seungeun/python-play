local start server
---
- python app.py


GCP
---
- https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579
- https://console.cloud.google.com/apis/dashboard?project=python-play-se

- pip install gcloud


- Cloud Build로 컨테이너 빌드
    - gcloud init
    - cd server
    - gcloud builds submit --tag gcr.io/python-play-se/check-blog-posts

- Cloud Run에 컨테이너 배포
    - gcloud beta run deploy --image gcr.io/python-play-se/check-blog-posts

- Cloud Run (fully managed)
- us-central1
- check-blog-posts


Firebase 호스팅 설정
---
- cd..
- npm을 통해 Firebase CLI 설치
    - npm init -y : package.json을 생성합니다. 
    - npm install -D firebase-tools

- firebase login

- firebase init hosting

- firebase server