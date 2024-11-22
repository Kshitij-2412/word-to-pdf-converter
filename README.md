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

3. **Run the Application**
   You have two options to run the application:

   Option 1 - Using run.sh script (recommended):
   ```bash
   # Start all services in background
   sh run.sh start

   # Start with visible logs
   sh run.sh start-with-logs

   # Check service status
   sh run.sh status

   # Stop all services
   sh run.sh stop

   # Run tests
   sh run.sh test
   ```

   Option 2 - Using Docker Compose directly:
   ```bash
   # Start all services with logs
   docker-compose up --build

   # Start in detached mode
   docker-compose up --build -d

   # Stop services
   docker-compose down
   ```

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

## Quick Start - Running from Docker Hub

The fastest way to run the application is to pull the images directly from Docker Hub. No need to clone the repository!

1. **Prerequisites**
   - Docker Desktop installed and running
   - 4GB RAM minimum
   - Ports 3000, 5000, 5001, and 5002 available

2. **Create Docker Network**
   ```bash
   docker network create rapidfort-net
   ```

3. **Create Volumes for Document Storage**
   ```bash
   docker volume create doc_uploads
   docker volume create doc_output
   ```

4. **Pull and Run the Services**

   a. Start Conversion Service:
   ```bash
   docker run -d --name conversion_service \
     --network rapidfort-net \
     -p 5002:5002 \
     -v doc_uploads:/app/uploads \
     -v doc_output:/app/output \
     -e FLASK_ENV=development \
     -e OUTPUT_FOLDER=/app/output \
     kshitijagarwal24/rapidfort-backend:conversion-service
   ```

   b. Start Upload Service:
   ```bash
   docker run -d --name upload_service \
     --network rapidfort-net \
     -p 5001:5001 \
     -v doc_uploads:/app/uploads \
     -e FLASK_ENV=development \
     -e UPLOAD_FOLDER=/app/uploads \
     kshitijagarwal24/rapidfort-backend:upload-service
   ```

   c. Start API Gateway:
   ```bash
   docker run -d --name api_gateway \
     --network rapidfort-net \
     -p 5000:5000 \
     -v doc_uploads:/app/uploads \
     -v doc_output:/app/output \
     -e FLASK_ENV=development \
     -e UPLOAD_SERVICE_URL=http://upload_service:5001 \
     -e CONVERSION_SERVICE_URL=http://conversion_service:5002 \
     kshitijagarwal24/rapidfort-backend:api-gateway
   ```

   d. Start Frontend:
   ```bash
   docker run -d --name frontend \
     --network rapidfort-net \
     -p 3000:3000 \
     -e REACT_APP_API_URL=http://localhost:5000/api \
     kshitijagarwal24/rapidfort-frontend:latest
   ```

5. **Access the Application**
   - Open your browser and go to: http://localhost:3000
   - You can now upload DOCX files and convert them to PDF

6. **Stop and Cleanup**
   ```bash
   # Stop all containers
   docker stop frontend api_gateway upload_service conversion_service

   # Remove containers
   docker rm frontend api_gateway upload_service conversion_service

   # Remove network
   docker network rm rapidfort-net

   # Remove volumes (optional - this will delete all uploaded and converted files)
   docker volume rm doc_uploads doc_output
   ```

## Kubernetes Deployment

### Prerequisites for Kubernetes Deployment
- Kubernetes cluster (minikube/kind/etc.)
- Ingress controller enabled
- kubectl installed and configured

### Deploying on Kubernetes

1. **Start your Kubernetes cluster**
   If using minikube:
   ```bash
   minikube start
   ```

2. **Enable Ingress Controller**
   For minikube:
   ```bash
   minikube addons enable ingress
   ```

3. **Deploy the Application**
   ```bash
   # Create namespace
   kubectl apply -f k8s/namespace.yaml

   # Create persistent volumes
   kubectl apply -f k8s/persistent-volumes.yaml

   # Deploy services
   kubectl apply -f k8s/api-gateway-deployment.yaml
   kubectl apply -f k8s/upload-service-deployment.yaml
   kubectl apply -f k8s/conversion-service-deployment.yaml
   kubectl apply -f k8s/frontend-deployment.yaml

   # Apply ingress configuration
   kubectl apply -f k8s/ingress.yaml
   ```

4. **Access the Application**
   If using minikube:
   ```bash
   # Start minikube tunnel in a separate terminal
   minikube tunnel
   ```
   
   The application will be available at:
   - Frontend: http://localhost/
   - API: http://localhost/api

### Verifying the Deployment

Check the status of your pods:
```bash
kubectl get pods -n rapidfort
```

Check the services:
```bash
kubectl get services -n rapidfort
```

Check the ingress:
```bash
kubectl get ingress -n rapidfort
```

### Troubleshooting Kubernetes Deployment

1. **Pod Issues**
   ```bash
   # Check pod status
   kubectl get pods -n rapidfort
   
   # Check pod logs
   kubectl logs -n rapidfort <pod-name>
   
   # Describe pod for more details
   kubectl describe pod -n rapidfort <pod-name>
   ```

2. **Service Issues**
   ```bash
   # Check service status
   kubectl get services -n rapidfort
   
   # Describe service
   kubectl describe service -n rapidfort <service-name>
   ```

3. **Ingress Issues**
   ```bash
   # Check ingress status
   kubectl get ingress -n rapidfort
   
   # Describe ingress
   kubectl describe ingress -n rapidfort
   ```

4. **Common Issues**
   - If pods are in "Pending" state, check if PersistentVolumes are properly configured
   - If pods are in "ImagePullBackOff", verify internet connection and image names
   - If services are not accessible, ensure minikube tunnel is running
   - If ingress is not working, verify that the ingress controller is enabled

## Docker Images

The application uses the following Docker Hub images:

- Frontend: `kshitijagarwal24/rapidfort-frontend:latest`
- Backend Services:
  * API Gateway: `kshitijagarwal24/rapidfort-backend:api-gateway`
  * Upload Service: `kshitijagarwal24/rapidfort-backend:upload-service`
  * Conversion Service: `kshitijagarwal24/rapidfort-backend:conversion-service`

You can pull these images directly:
```bash
# Pull frontend
docker pull kshitijagarwal24/rapidfort-frontend:latest

# Pull backend services
docker pull kshitijagarwal24/rapidfort-backend:api-gateway
docker pull kshitijagarwal24/rapidfort-backend:upload-service
docker pull kshitijagarwal24/rapidfort-backend:conversion-service
```

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
├── docker-compose.yml      # Docker composition config
└── run.sh                  # Application management script
