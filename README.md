docker build -t usatpath01/vulnerable-photo-app-frontend:latest ./frontend
docker build -t usatpath01/vulnerable-photo-app-api-gateway:latest ./api_gateway
docker build -t usatpath01/vulnerable-photo-app-user-service:latest ./user_service
docker build -t usatpath01/vulnerable-photo-app-photo-service:latest ./photo_service
docker build -t usatpath01/vulnerable-photo-app-notification-service:latest ./notification_service
docker build -t usatpath01/vulnerable-photo-app-recommendation-service:latest ./recommendation_service
docker build -t usatpath01/vulnerable-photo-app-analytics-service:latest ./analytics_service


docker push usatpath01/vulnerable-photo-app-frontend:latest
docker push usatpath01/vulnerable-photo-app-api-gateway:latest
docker push usatpath01/vulnerable-photo-app-user-service:latest
docker push usatpath01/vulnerable-photo-app-photo-service:latest
docker push usatpath01/vulnerable-photo-app-notification-service:latest
docker push usatpath01/vulnerable-photo-app-recommendation-service:latest
docker push usatpath01/vulnerable-photo-app-analytics-service:latest





docker tag usatpath01/vulnerable-photo-app-analytics-service:v1 usatpath01/vulnerable-photo-app-analytics-service:v1
docker tag usatpath01/vulnerable-photo-app-notification-service:v1 usatpath01/vulnerable-photo-app-notification-service:v1
docker tag usatpath01/vulnerable-photo-app-api_gateway:v1 usatpath01/vulnerable-photo-app-api_gateway:v1
docker tag usatpath01/vulnerable-photo-app-frontend-service:v1 usatpath01/vulnerable-photo-app-frontend-service:v1
docker tag usatpath01/vulnerable-photo-app-photo-service:v1 usatpath01/vulnerable-photo-app-photo-service:v1
docker tag usatpath01/vulnerable-photo-app-recommedation-service:v1 usatpath01/vulnerable-photo-app-recommedation-service:v1
docker tag usatpath01/vulnerable-photo-app-user-service:v1 usatpath01/vulnerable-photo-app-user-service:v1