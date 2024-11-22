#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
}

# Function to run the application
run_app() {
    echo -e "${GREEN}Starting the application...${NC}"
    docker-compose up --build $1
}

# Function to stop the application
stop_app() {
    echo -e "${GREEN}Stopping the application...${NC}"
    docker-compose down
}

# Function to show application status
show_status() {
    echo -e "${GREEN}Application URLs:${NC}"
    echo "Frontend: http://localhost:3000"
    echo "API Gateway: http://localhost:5000"
    echo "Upload Service: http://localhost:5001"
    echo "Conversion Service: http://localhost:5002"
    
    echo -e "\n${GREEN}Container Status:${NC}"
    docker-compose ps
}

# Function to run tests
run_tests() {
    echo -e "${GREEN}Running tests...${NC}"
    docker-compose exec api-gateway python -m unittest discover -s ./tests -p 'test_*.py'
}

# Main script
case "$1" in
    "start")
        check_docker
        run_app "-d"  # Run in detached mode
        sleep 5  # Wait for containers to start
        show_status
        ;;
    "start-with-logs")
        check_docker
        run_app ""  # Run with logs visible
        ;;
    "stop")
        check_docker
        stop_app
        ;;
    "status")
        check_docker
        show_status
        ;;
    "test")
        check_docker
        run_app "-d"  # Run in detached mode
        sleep 5  # Wait for containers to start
        run_tests
        stop_app
        ;;
    *)
        echo "Usage: $0 {start|start-with-logs|stop|status|test}"
        echo "  start:          Start all services in the background"
        echo "  start-with-logs: Start all services and show logs"
        echo "  stop:           Stop all services"
        echo "  status:         Show the status of all services"
        echo "  test:           Run tests"
        exit 1
        ;;
esac
