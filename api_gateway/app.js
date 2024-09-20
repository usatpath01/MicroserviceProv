// api_gateway/app.js
const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();
const port = 8000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
const userServiceProxy = createProxyMiddleware({
  target: 'http://user_service:5000',
  changeOrigin: true,
  pathRewrite: {'^/api/users': '/api/v1/users'},
});

const photoServiceProxy = createProxyMiddleware({
  target: 'http://photo_service:5000',
  changeOrigin: true,
  pathRewrite: {'^/api/photos': ''},
});

const notificationServiceProxy = createProxyMiddleware({
  target: 'http://notification_service:5000',
  changeOrigin: true,
  pathRewrite: {'^/api/notifications': ''},
});

const recommendationServiceProxy = createProxyMiddleware({
  target: 'http://recommendation_service:5000',
  changeOrigin: true,
  pathRewrite: {'^/api/recommendations': ''},
});

const analyticsServiceProxy = createProxyMiddleware({
  target: 'http://analytics_service:5000',
  changeOrigin: true,
  pathRewrite: {'^/api/analytics': ''},
});

app.use('/api/users', userServiceProxy);
app.use('/api/photos', photoServiceProxy);
app.use('/api/notifications', notificationServiceProxy);
app.use('/api/recommendations', recommendationServiceProxy);
app.use('/api/analytics', analyticsServiceProxy);

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK' });
});

// Vulnerability: Sensitive Data Exposure
app.get('/api/debug', (req, res) => {
  res.json({
    environment: process.env,
    services: {
      user_service: 'http://user_service:5000',
      photo_service: 'http://photo_service:5000',
      notification_service: 'http://notification_service:5000',
      recommendation_service: 'http://recommendation_service:5000',
      analytics_service: 'http://analytics_service:5000'
    }
  });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke in the API Gateway!');
});

app.listen(port, () => {
  console.log(`API Gateway listening at http://localhost:${port}`);
});