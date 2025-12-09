#!/bin/bash

# Bookstore-R-Us Local Development Script
# Starts all Python microservices and the Next.js frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DB_PORT=${DB_PORT:-5433}
DB_NAME=${DB_NAME:-postgres}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-password}
DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@localhost:${DB_PORT}/${DB_NAME}"

FRONTEND_PORT=${FRONTEND_PORT:-1123}
API_GATEWAY_PORT=8081
PRODUCTS_PORT=8082
CART_PORT=8083
CHECKOUT_PORT=8084
LOGIN_PORT=8085

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Bookstore-R-Us Local Development${NC}"
echo -e "${GREEN}========================================${NC}"

# Function to check if a port is in use
check_port() {
    lsof -i ":$1" >/dev/null 2>&1
}

# Function to kill process on a port
kill_port() {
    local port=$1
    if check_port "$port"; then
        echo -e "${YELLOW}Killing existing process on port $port${NC}"
        lsof -ti ":$port" | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
}

# Function to wait for a service to be ready
wait_for_service() {
    local port=$1
    local name=$2
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if check_port "$port"; then
            echo -e "${GREEN}$name is ready on port $port${NC}"
            return 0
        fi
        sleep 1
        ((attempt++))
    done

    echo -e "${RED}$name failed to start on port $port${NC}"
    return 1
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    pkill -f "uvicorn main:app" 2>/dev/null || true
    pkill -f "next dev" 2>/dev/null || true
    echo -e "${GREEN}Services stopped${NC}"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Check for required tools
echo -e "\n${YELLOW}Checking prerequisites...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}python3 is required but not installed${NC}"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo -e "${RED}node is required but not installed${NC}"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm is required but not installed${NC}"
    exit 1
fi

echo -e "${GREEN}Prerequisites OK${NC}"

# Install Python dependencies if needed
echo -e "\n${YELLOW}Checking Python dependencies...${NC}"
pip3 install uvicorn fastapi sqlmodel psycopg2-binary httpx py-eureka-client python-multipart "passlib[bcrypt]" "python-jose[cryptography]" --quiet 2>/dev/null || {
    echo -e "${YELLOW}Installing Python dependencies...${NC}"
    pip3 install uvicorn fastapi sqlmodel psycopg2-binary httpx py-eureka-client python-multipart "passlib[bcrypt]" "python-jose[cryptography]"
}
echo -e "${GREEN}Python dependencies OK${NC}"

# Kill any existing services on our ports
echo -e "\n${YELLOW}Cleaning up existing services...${NC}"
kill_port $API_GATEWAY_PORT
kill_port $PRODUCTS_PORT
kill_port $CART_PORT
kill_port $CHECKOUT_PORT
kill_port $LOGIN_PORT
kill_port $FRONTEND_PORT

# Start Python microservices
echo -e "\n${YELLOW}Starting Python microservices...${NC}"

# Products Service
echo "Starting Products Service on port $PRODUCTS_PORT..."
cd "$SCRIPT_DIR/python-services/products-service"
DATABASE_URL="$DATABASE_URL" python3 -m uvicorn main:app --host 0.0.0.0 --port $PRODUCTS_PORT &
PRODUCTS_PID=$!

# Cart Service
echo "Starting Cart Service on port $CART_PORT..."
cd "$SCRIPT_DIR/python-services/cart-service"
DATABASE_URL="$DATABASE_URL" python3 -m uvicorn main:app --host 0.0.0.0 --port $CART_PORT &
CART_PID=$!

# Checkout Service
echo "Starting Checkout Service on port $CHECKOUT_PORT..."
cd "$SCRIPT_DIR/python-services/checkout-service"
DATABASE_URL="$DATABASE_URL" \
PRODUCTS_SERVICE_URL="http://localhost:$PRODUCTS_PORT/products-microservice" \
CART_SERVICE_URL="http://localhost:$CART_PORT/cart-microservice" \
python3 -m uvicorn main:app --host 0.0.0.0 --port $CHECKOUT_PORT &
CHECKOUT_PID=$!

# Login Service
echo "Starting Login Service on port $LOGIN_PORT..."
cd "$SCRIPT_DIR/python-services/login-service"
DATABASE_URL="$DATABASE_URL" python3 -m uvicorn main:app --host 0.0.0.0 --port $LOGIN_PORT &
LOGIN_PID=$!

# Wait for backend services to be ready
sleep 2

# API Gateway
echo "Starting API Gateway on port $API_GATEWAY_PORT..."
cd "$SCRIPT_DIR/python-services/api-gateway"
PRODUCTS_SERVICE_URL="http://localhost:$PRODUCTS_PORT" \
CART_SERVICE_URL="http://localhost:$CART_PORT" \
CHECKOUT_SERVICE_URL="http://localhost:$CHECKOUT_PORT" \
LOGIN_SERVICE_URL="http://localhost:$LOGIN_PORT" \
python3 -m uvicorn main:app --host 0.0.0.0 --port $API_GATEWAY_PORT &
API_GATEWAY_PID=$!

# Wait for API Gateway
wait_for_service $API_GATEWAY_PORT "API Gateway"

# Start Next.js frontend
echo -e "\n${YELLOW}Starting Next.js frontend...${NC}"
cd "$SCRIPT_DIR/nextjs-frontend"

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

NEXT_PUBLIC_API_URL="http://localhost:$API_GATEWAY_PORT" npm run dev -- -p $FRONTEND_PORT &
FRONTEND_PID=$!

# Wait for frontend
wait_for_service $FRONTEND_PORT "Next.js Frontend"

# Open browser (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "\n${YELLOW}Opening browser...${NC}"
    sleep 2
    open -a "Google Chrome" "http://localhost:$FRONTEND_PORT" 2>/dev/null || open "http://localhost:$FRONTEND_PORT"
fi

# Print status
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  All services are running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e ""
echo -e "  Frontend:        http://localhost:$FRONTEND_PORT"
echo -e "  API Gateway:     http://localhost:$API_GATEWAY_PORT"
echo -e "  Products:        http://localhost:$PRODUCTS_PORT"
echo -e "  Cart:            http://localhost:$CART_PORT"
echo -e "  Checkout:        http://localhost:$CHECKOUT_PORT"
echo -e "  Login:           http://localhost:$LOGIN_PORT"
echo -e ""
echo -e "  Database:        $DATABASE_URL"
echo -e ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo -e ""

# Keep script running and wait for all background processes
wait
