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

## Prerequisites

Before running this project, make sure you have the following installed on your system:

1. **Docker Desktop**
   - Download and install from [Docker Official Website](https://www.docker.com/products/docker-desktop/)
   - Make sure Docker Desktop is running before starting the project
   - Minimum requirements:
     * Windows 10/11 Pro or Enterprise (for Windows users)
     * macOS 10.15 or newer (for Mac users)
     * 4GB RAM minimum
     * Enable virtualization in BIOS (for Windows users)

2. **Git**
   - Download and install from [Git Official Website](https://git-scm.com/downloads)
   - Required for cloning the repository

3. **Web Browser**
   - Any modern web browser (Chrome, Firefox, Edge, etc.)
   - Required for accessing the web interface

## Quick Start Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kshitij-2412/word-to-pdf-converter.git
   cd word-to-pdf-converter
   ```

2. **Start Docker Desktop**
   - Make sure Docker Desktop is running on your system
   - You should see the Docker icon in your system tray (Windows) or menu bar (Mac)

3. **Build and Start the Application**
   ```bash
   docker-compose up --build
   ```
   - This command will:
     * Download necessary Docker images
     * Build all services (frontend, api_gateway, upload_service, conversion_service)
     * Start all containers
     * This process might take a few minutes on first run

4. **Access the Application**
   - Open your web browser and go to:
     * Frontend UI: http://localhost:3000
   - The API services will be running at:
     * API Gateway: http://localhost:5000
     * Upload Service: http://localhost:5001
     * Conversion Service: http://localhost:5002

5. **Using the Application**
   - Upload a DOCX file using the web interface
   - Optionally set a password for PDF protection
   - Click Convert to start the conversion process
   - Download your converted PDF file

## Troubleshooting

If you encounter any issues:

1. **Docker Issues**
   - Make sure Docker Desktop is running
   - Try restarting Docker Desktop
   - Run `docker-compose down` followed by `docker-compose up --build`

2. **Port Conflicts**
   - Ensure ports 3000, 5000, 5001, and 5002 are not being used by other applications
   - To check ports in use:
     * Windows: `netstat -ano | findstr PORT_NUMBER`
     * Mac/Linux: `lsof -i :PORT_NUMBER`

3. **Common Fixes**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild containers: `docker-compose build --no-cache`
   - Remove all containers and volumes:
     ```bash
     docker-compose down -v
     docker-compose up --build
     ```

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

## Project Structure
```
.
├── frontend/                 # React frontend application
├── backend/                 # Backend services
│   ├── api_gateway/        # API Gateway service
│   ├── upload_service/     # Upload handling service
│   └── conversion_service/ # Document conversion service
└── docker-compose.yml      # Docker composition config
```

## Development

For development purposes, you can run individual services:

```bash
# Start all services
docker-compose up --build

# Start individual services
docker-compose up --build frontend
docker-compose up --build api_gateway
docker-compose up --build upload_service
docker-compose up --build conversion_service
```

