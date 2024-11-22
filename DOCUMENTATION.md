# Rapid Fort Document Converter - Visual Guide

This guide provides a visual walkthrough of the Rapid Fort Document Converter application, showing how to use its features and what to expect at each step.

## Application Interface & Features

### 1. Home Page
![Home Page](screenshots/home-page.png)
The home page provides a clean and intuitive interface with:
- File upload button to select your DOCX document
- Password protection option for securing your PDF
- Convert button to start the conversion process
- Status display area for conversion progress

### 2. Password Protection Feature
![Password Protection](screenshots/password-protection-feature.png)
Adding security to your PDF:
1. Click "Choose File" to select your DOCX document
2. Enter a password in the "Password Protection" field
3. Click "Convert" to create a password-protected PDF

### 3. Successful Conversion
![Successful Conversion](screenshots/successfull-conversion.png)
When conversion completes successfully:
- Success message is displayed
- Download button appears
- File details are shown
- Original and converted file sizes are displayed

### 4. Encrypted File Result
![Encrypted File](screenshots/encrypted-file.png)
When opening a password-protected PDF:
- PDF reader will prompt for the password
- File remains secure until correct password is entered
- Prevents unauthorized access to sensitive documents

## Service Architecture

The application uses a microservices architecture with four main components:

1. **Frontend Service** (Port 3000)
   - React-based user interface
   - Handles file selection and user interactions
   - Displays conversion progress and results

2. **API Gateway** (Port 5000)
   - Routes requests between services
   - Manages file upload coordination
   - Handles response aggregation

3. **Upload Service** (Port 5001)
   - Processes file uploads
   - Validates file formats
   - Manages temporary storage

4. **Conversion Service** (Port 5002)
   - Converts DOCX to PDF
   - Implements password protection
   - Optimizes output files

## Running the Application

You can run the application in two ways:

### 1. Quick Start with Docker Hub
Pull and run directly from Docker Hub:
```bash
# Create network and volumes
docker network create rapidfort-net
docker volume create doc_uploads
docker volume create doc_output

# Run the services
docker run -d --name conversion_service --network rapidfort-net -p 5002:5002 -v doc_uploads:/app/uploads -v doc_output:/app/output -e FLASK_ENV=development -e OUTPUT_FOLDER=/app/output kshitijagarwal24/rapidfort-backend:conversion-service

docker run -d --name upload_service --network rapidfort-net -p 5001:5001 -v doc_uploads:/app/uploads -e FLASK_ENV=development -e UPLOAD_FOLDER=/app/uploads kshitijagarwal24/rapidfort-backend:upload-service

docker run -d --name api_gateway --network rapidfort-net -p 5000:5000 -v doc_uploads:/app/uploads -v doc_output:/app/output -e FLASK_ENV=development -e UPLOAD_SERVICE_URL=http://upload_service:5001 -e CONVERSION_SERVICE_URL=http://conversion_service:5002 kshitijagarwal24/rapidfort-backend:api-gateway

docker run -d --name frontend --network rapidfort-net -p 3000:3000 -e REACT_APP_API_URL=http://localhost:5000/api kshitijagarwal24/rapidfort-frontend:latest
```

### 2. Development Setup
Clone and run with docker-compose:
```bash
git clone https://github.com/Kshitij-2412/word-to-pdf-converter.git
cd word-to-pdf-converter
docker-compose up --build
```

## Troubleshooting Tips

1. **Service Connectivity Issues**
   - Ensure all containers are running: `docker ps`
   - Check service logs: `docker logs [container_name]`
   - Verify network connectivity: `docker network inspect rapidfort-net`

2. **File Upload Problems**
   - Check volume permissions
   - Verify file format is DOCX
   - Ensure sufficient disk space

3. **Conversion Errors**
   - Check conversion service logs
   - Verify file is not corrupted
   - Ensure all services are healthy

## Cleanup

When you're done using the application:
```bash
# Stop all containers
docker stop frontend api_gateway upload_service conversion_service

# Remove containers
docker rm frontend api_gateway upload_service conversion_service

# Remove network and volumes
docker network rm rapidfort-net
docker volume rm doc_uploads doc_output
