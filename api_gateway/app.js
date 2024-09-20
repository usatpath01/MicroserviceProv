// api_gateway/app.js
const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');
const app = express();
const multer = require('multer');
const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');


const port = 8000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/')
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname))
  }
});

const upload = multer({ dest: 'uploads/' });

const userServiceProxy = createProxyMiddleware({
  target: 'http://user_service:5000',
  changeOrigin: true,
  pathRewrite: {'^/api/users': '/api/v1/users'},
  onProxyReq: (proxyReq, req, res) => {
    if (req.body) {
      let bodyData = JSON.stringify(req.body);
      proxyReq.setHeader('Content-Type', 'application/json');
      proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
      proxyReq.write(bodyData);
    }
  },
  onProxyRes: (proxyRes, req, res) => {
    console.log(`Received response from user service: ${proxyRes.statusCode}`);
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.status(500).json({ error: 'Proxy error', message: err.message });
  }
});



const photoServiceProxy = createProxyMiddleware({
  target: 'http://photo_service:5000',
  changeOrigin: true,
  pathRewrite: {'^/api/photos': '/api/v1/photos'},
  onProxyReq: (proxyReq, req, res) => {
    console.log(`Proxying ${req.method} request to: ${proxyReq.path}`);
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.status(500).json({ status: 'error', message: 'Proxy error occurred' });
  }
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

app.post('/api/photos/upload', upload.single('file'), async (req, res) => {
  console.log('Received file upload request');
  console.log('File:', req.file);
  console.log('Body:', req.body);

  if (!req.file) {
    return res.status(400).json({ status: 'error', message: 'No file uploaded' });
  }

  const form = new FormData();
  form.append('file', fs.createReadStream(req.file.path), {
    filename: req.file.originalname,
    contentType: req.file.mimetype
  });
  form.append('user_id', req.body.user_id);

  try {
    const response = await axios.post('http://photo_service:5000/api/v1/photos/upload', form, {
      headers: {
        ...form.getHeaders()
      }
    });

    console.log('Photo Service Response:', response.data);
    res.json(response.data);
  } catch (error) {
    console.error('Error sending request to Photo Service:', error.response ? error.response.data : error.message);
    res.status(500).json({ status: 'error', message: 'Internal server error' });
  }
});


app.use('/api/photos', photoServiceProxy);

app.use('/api/notifications', notificationServiceProxy);
app.use('/api/recommendations', recommendationServiceProxy);
app.use('/api/analytics', analyticsServiceProxy);

app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  console.log(`Received request: ${req.method} ${req.url}`);
  next();
});

app.get('/health', (req, res) => {
  console.log("Health check request received");
  res.status(200).json({ status: 'healthy' });
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
  //res.status(500).send('Something broke in the API Gateway!');
  console.error('Error:', err);
  res.status(500).json({ error: 'Internal server error', message: err.message });
});

app.listen(port, () => {
  console.log(`API Gateway listening at http://localhost:${port}`);
});