```
docker build -t usatpath01/vulnerable-photo-app-frontend:latest ./frontend
docker build -t usatpath01/vulnerable-photo-app-api-gateway:latest ./api_gateway
docker build -t usatpath01/vulnerable-photo-app-user-service:latest ./user_service
docker build -t usatpath01/vulnerable-photo-app-photo-service:latest ./photo_service
docker build -t usatpath01/vulnerable-photo-app-notification-service:latest ./notification_service
docker build -t usatpath01/vulnerable-photo-app-recommendation-service:latest ./recommendation_service
docker build -t usatpath01/vulnerable-photo-app-analytics-service:latest ./analytics_service
```
```
docker push usatpath01/vulnerable-photo-app-frontend:latest
docker push usatpath01/vulnerable-photo-app-api-gateway:latest
docker push usatpath01/vulnerable-photo-app-user-service:latest
docker push usatpath01/vulnerable-photo-app-photo-service:latest
docker push usatpath01/vulnerable-photo-app-notification-service:latest
docker push usatpath01/vulnerable-photo-app-recommendation-service:latest
docker push usatpath01/vulnerable-photo-app-analytics-service:latest
```

```
from api container
apk add curl
curl http://user_service:5000/api/v1/users/test-db-connection
```

```
docker exec -it e38172ae10a5 mysql -uroot -pinsecure_password
USE users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE
);
INSERT INTO users (username, password, email) VALUES ('testuser', 'testpassword', 'testuser@example.com');
```

```
CREATE TABLE IF NOT EXISTS photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

INSERT INTO photos (filename, user_id, upload_date) VALUES ('docker.png', 1, '2001-09-10');

```



# Endpoint
```
curl -X POST "http://10.5.20.45:8000/api/users/login"      -H "Content-Type: application/json"      -d '{"username":"testuser","password":"testpassword"}'
{
  "message": "Login successful", 
  "status": "success", 
  "user": {
    "email": "testuser@example.com", 
    "id": 1, 
    "username": "testuser"
  }
}

curl -X POST "http://10.5.20.45:8000/api/users/login"      -H "Content-Type: application/json"      -d '{"username":"testuser","password":"testpasswossrd"}'
{
  "message": "Invalid credentials", 
  "status": "error"
}

curl -X POST "http://10.5.20.45:8000/api/users/register"      -H "Content-Type: application/json"      -d '{"username":"newuser", "password":"newpassword", "email":"newuser@example.com"}'
{
  "message": "User registered successfully", 
  "status": "success", 
  "user": {
    "email": "newuser@example.com", 
    "id": 1, 
    "username": "newuser"
  }
}


curl -X POST "http://10.5.20.45:8000/api/photos/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@Docker.png" \
     -F "user_id=1"

{
  "filename": "9e210176-6c49-42c4-8e44-136642a0b275.png", 
  "message": "File uploaded successfully", 
  "status": "success"
}

curl -X GET "http://10.5.20.45:8000/api/photos/Docker.png"
```

```
docker tag usatpath01/vulnerable-photo-app-analytics-service:v1 usatpath01/vulnerable-photo-app-analytics-service:v1
docker tag usatpath01/vulnerable-photo-app-notification-service:v1 usatpath01/vulnerable-photo-app-notification-service:v1
docker tag usatpath01/vulnerable-photo-app-api_gateway:v1 usatpath01/vulnerable-photo-app-api_gateway:v1
docker tag usatpath01/vulnerable-photo-app-frontend-service:v1 usatpath01/vulnerable-photo-app-frontend-service:v1
docker tag usatpath01/vulnerable-photo-app-photo-service:v1 usatpath01/vulnerable-photo-app-photo-service:v1
docker tag usatpath01/vulnerable-photo-app-recommedation-service:v1 usatpath01/vulnerable-photo-app-recommedation-service:v1
docker tag usatpath01/vulnerable-photo-app-user-service:v1 usatpath01/vulnerable-photo-app-user-service:v1
```
```
git push -u origin main
```