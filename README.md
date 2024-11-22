# Document Converter Platform

A robust microservices-based document conversion platform that converts DOCX files to PDF with optional password protection. Built with React frontend and Flask backend services, containerized with Docker for easy deployment.

## Features

- DOCX to PDF conversion
- Optional PDF password protection
- Microservices architecture
- Docker containerization
- Cross-platform compatibility
- Responsive web interface
- Fast and efficient processing

## Architecture

The application consists of three main microservices:
1. **API Gateway** - Routes requests and handles client communication
2. **Upload Service** - Manages file uploads and storage
3. **Conversion Service** - Handles document conversion and PDF protection

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Kshitij-2412/word-to-pdf-converter.git
```

2. Start the application:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:3000
- API Gateway: http://localhost:5000

## API Endpoints

### API Gateway (Port 5000)
- `POST /api/upload` - Upload DOCX file
- `POST /api/convert` - Convert DOCX to PDF
- `GET /api/download/{filename}` - Download converted PDF

### Upload Service (Port 5001)
- `POST /upload` - Handle file upload

### Conversion Service (Port 5002)
- `POST /convert` - Convert documents
- `POST /protect` - Add password protection to PDF

## Development

### Project Structure
```
.
├── frontend/                 # React frontend application
├── backend/                 # Backend services
│   ├── api_gateway/        # API Gateway service
│   ├── upload_service/     # Upload handling service
│   └── conversion_service/ # Document conversion service
└── docker-compose.yml      # Docker composition config
```

### Environment Variables
All necessary environment variables are included in the repository for easy setup.

### Building for Development
```bash
# Start all services
docker-compose up --build

# Start individual services
docker-compose up --build frontend
docker-compose up --build api_gateway
docker-compose up --build upload_service
docker-compose up --build conversion_service
```

