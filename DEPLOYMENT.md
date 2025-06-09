# Dream Visualizer - Production Deployment Guide

This guide covers deploying the Dream Visualizer application in a production environment.

## 🚀 Quick Start (Production)

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Dream-Visualiser-api
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
DATABASE_URL=sqlite:///./dream_visualizer.db
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MODEL_PATH=
HOST=0.0.0.0
PORT=8000
WORKERS=1
```

**⚠️ Important**: Change the `JWT_SECRET` to a secure, random string in production!

### 3. Start Production Servers

```bash
./start_production.sh
```

This will:

- Install backend dependencies
- Build the frontend
- Start the backend API server
- Serve the frontend static files
- Display server URLs

### 4. Stop Servers

```bash
./stop_production.sh
```

## 📋 Manual Deployment

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run_production.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run build
cd dist
python3 -m http.server 3000
```

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL`: Database connection string
- `JWT_SECRET`: Secret key for JWT tokens (CHANGE IN PRODUCTION!)
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `WORKERS`: Number of worker processes

### Database

The application uses SQLite by default. For production, consider:

- PostgreSQL for better performance
- Regular database backups
- Database connection pooling

## 🛡️ Security Considerations

### Before Production:

1. **Change JWT Secret**: Generate a secure random string
2. **HTTPS**: Use a reverse proxy (nginx/Apache) with SSL
3. **Firewall**: Restrict access to necessary ports only
4. **Updates**: Keep dependencies updated
5. **Monitoring**: Set up logging and monitoring

### Generate Secure JWT Secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🌐 Reverse Proxy Setup (nginx)

### nginx Configuration Example:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Static files
    location /static/ {
        proxy_pass http://localhost:8000;
    }
}
```

## 📊 Monitoring and Logs

### Application Logs

- Backend logs are output to stdout with timestamps
- Frontend access logs via Python HTTP server
- Configure log rotation for production

### Health Checks

- Backend: `GET /health`
- Frontend: `GET /` (returns 200 if serving)

### Monitoring Endpoints

- API Documentation: `http://localhost:8000/docs`
- API Health: `http://localhost:8000/health`

## 🐳 Docker Deployment (Alternative)

For containerized deployment, create these files:

### Dockerfile (Backend)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "run_production.py"]
```

### Docker Compose

```yaml
version: "3.8"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./dream_visualizer.db
      - JWT_SECRET=your-secure-secret
    volumes:
      - ./data:/app/data

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
```

## 🔍 Troubleshooting

### Common Issues:

1. **Port Already in Use**

   ```bash
   lsof -ti:8000 | xargs kill -9  # Kill process on port 8000
   ```

2. **Permission Denied on Scripts**

   ```bash
   chmod +x start_production.sh stop_production.sh
   ```

3. **Module Not Found**

   - Ensure virtual environment is activated
   - Install dependencies: `pip install -r requirements.txt`

4. **Frontend Build Fails**
   - Check Node.js version: `node --version`
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### Logs Location:

- Backend: stdout (captured by process manager)
- Frontend: Python HTTP server logs
- Check server status: `ps aux | grep python`

## 📈 Performance Optimization

### Backend:

- Use multiple workers: Set `WORKERS=4` in `.env`
- Database connection pooling
- Redis for caching (optional)

### Frontend:

- Use nginx/Apache for static file serving
- Enable gzip compression
- CDN for static assets

## 🔄 Updates and Maintenance

### Update Application:

```bash
git pull
./stop_production.sh
pip install -r backend/requirements.txt
cd frontend && npm install && npm run build && cd ..
./start_production.sh
```

### Database Backup:

```bash
cp backend/dream_visualizer.db backup_$(date +%Y%m%d).db
```

## 📞 Support

For production issues:

1. Check logs for error messages
2. Verify environment configuration
3. Ensure all dependencies are installed
4. Check firewall and network settings

---

**Last Updated**: January 2025
