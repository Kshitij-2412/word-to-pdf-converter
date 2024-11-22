# Document Converter

A robust microservices-based document conversion platform that converts DOCX files to password-protected PDFs.

## Features

- DOCX to PDF conversion with LibreOffice
- Secure PDF password protection using PyPDF2
- Modern React-based frontend with drag-and-drop
- Microservices architecture with Docker containerization
- Real-time conversion progress tracking
- Secure file handling and cleanup

## Architecture

The application consists of four main components:
- Frontend (React, port 3000)
- API Gateway (Flask, port 5000)
- Upload Service (Flask, port 5001)
- Conversion Service (Flask, port 5002)

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for frontend development)
- Python 3.9+ (for backend development)
- LibreOffice (installed in conversion service container)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/document-converter.git
cd document-converter
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application:
   - Open http://localhost:3000 in your browser
   - Upload a DOCX file
   - Optionally set a password for PDF protection
   - Click Convert
   - Download and open the converted PDF

## Development Setup

### Frontend
```bash
cd frontend
npm install
npm start
```

### Backend Services
```bash
# API Gateway
cd backend/api_gateway
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
flask run --port 5000

# Similar steps for upload_service and conversion_service
```

## Environment Configuration

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

### Backend (docker-compose.yml)
```
UPLOAD_SERVICE_URL=http://upload_service:5001
CONVERSION_SERVICE_URL=http://conversion_service:5002
```

## Docker Deployment

Build and run all services:
```bash
docker-compose up --build -d
```

Individual services:
```bash
docker-compose up --build -d frontend
docker-compose up --build -d api_gateway
docker-compose up --build -d upload_service
docker-compose up --build -d conversion_service
```

## Security Features

- PDF password protection using industry-standard encryption
- Secure file handling with automatic cleanup
- CORS configuration for secure cross-origin requests
- Environment-based configuration management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)
