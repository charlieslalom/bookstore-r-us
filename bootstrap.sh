#!/bin/bash

# Bootstrap script for Yugastore Java application
# This script follows the "Running the app on host" instructions from README.md

# Configuration
LOG_FILE="bootstrap.log"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# Initialize log file
echo "=== Yugastore Bootstrap Log ===" > "$LOG_FILE"
echo "Started at: $(date)" >> "$LOG_FILE"
echo "Working directory: $BASE_DIR" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Function to map common exit codes to descriptions
get_exit_code_description() {
    local code=$1
    case $code in
        0) echo "Success" ;;
        1) echo "General error" ;;
        2) echo "Misuse of shell command" ;;
        126) echo "Command invoked cannot execute (permission problem or not executable)" ;;
        127) echo "Command not found" ;;
        128) echo "Invalid argument to exit" ;;
        130) echo "Script terminated by Ctrl+C" ;;
        137) echo "Process killed (SIGKILL)" ;;
        139) echo "Segmentation fault (SIGSEGV)" ;;
        143) echo "Process terminated (SIGTERM)" ;;
        255) echo "Exit status out of range" ;;
        *) echo "Unknown error code" ;;
    esac
}

# Function to run a command with logging
run_command() {
    local description="$1"
    local command="$2"
    local working_dir="${3:-$BASE_DIR}"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] RUNNING: $description" >> "$LOG_FILE"
    echo "  Command: $command" >> "$LOG_FILE"
    echo "  Directory: $working_dir" >> "$LOG_FILE"

    # Run command and capture output and exit code
    cd "$working_dir"
    output=$(eval "$command" 2>&1)
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "  Status: SUCCESS" >> "$LOG_FILE"
    else
        local error_desc=$(get_exit_code_description $exit_code)
        echo "  Status: FAILURE" >> "$LOG_FILE"
        echo "  Exit Code: $exit_code ($error_desc)" >> "$LOG_FILE"
        echo "  Error Output: $output" >> "$LOG_FILE"
    fi
    echo "" >> "$LOG_FILE"

    cd "$BASE_DIR"
    return $exit_code
}

# Function to run a background service with logging
run_service_background() {
    local description="$1"
    local command="$2"
    local working_dir="${3:-$BASE_DIR}"
    local log_prefix="$4"

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] STARTING SERVICE: $description" >> "$LOG_FILE"
    echo "  Command: $command" >> "$LOG_FILE"
    echo "  Directory: $working_dir" >> "$LOG_FILE"

    cd "$working_dir"
    nohup $command > "${BASE_DIR}/${log_prefix}.out" 2>&1 &
    local pid=$!

    # Give the service a moment to start or fail immediately
    sleep 3

    if ps -p $pid > /dev/null 2>&1; then
        echo "  Status: SUCCESS (PID: $pid)" >> "$LOG_FILE"
        echo "  Service output logged to: ${log_prefix}.out" >> "$LOG_FILE"
    else
        wait $pid 2>/dev/null
        exit_code=$?
        local error_desc=$(get_exit_code_description $exit_code)
        echo "  Status: FAILURE" >> "$LOG_FILE"
        echo "  Exit Code: $exit_code ($error_desc)" >> "$LOG_FILE"
        echo "  Error Output: $(tail -20 ${BASE_DIR}/${log_prefix}.out 2>/dev/null)" >> "$LOG_FILE"
    fi
    echo "" >> "$LOG_FILE"

    cd "$BASE_DIR"
}

echo "Starting Yugastore bootstrap..."
echo "Log file: $LOG_FILE"
echo ""

# Build the application
echo "Building the application..."
run_command "Build application with Maven" "mvn -DskipTests package"
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed. Check $LOG_FILE for details."
    exit 1
fi

# Step 1: Initialize YugabyteDB - Create CQL schema
echo "Step 1: Initializing YugabyteDB..."
run_command "Create CQL schema" "cqlsh -f schema.cql" "$BASE_DIR/resources"
if [ $? -ne 0 ]; then
    echo "WARNING: CQL schema creation failed. Is YugabyteDB running? Check $LOG_FILE for details."
fi

# Step 1: Load sample data
echo "Loading sample data..."
run_command "Load sample data" "./dataload.sh" "$BASE_DIR/resources"
if [ $? -ne 0 ]; then
    echo "WARNING: Data load failed. Check $LOG_FILE for details."
fi

# Step 1: Create PostgreSQL/YSQL tables
echo "Creating YSQL tables..."
run_command "Create YSQL schema" "psql -h localhost -p 5433 -U yugabyte -d yugabyte -f schema.sql" "$BASE_DIR/resources"
if [ $? -ne 0 ]; then
    echo "WARNING: YSQL schema creation failed. Check $LOG_FILE for details."
fi

# Step 2: Start Eureka service discovery
echo "Step 2: Starting Eureka service discovery..."
run_service_background "Eureka Service Discovery" "mvn spring-boot:run" "$BASE_DIR/eureka-server-local" "eureka-server"
echo "Waiting for Eureka to initialize (30 seconds)..."
sleep 30

# Step 2 (continued): Start API Gateway microservice
echo "Starting API Gateway microservice..."
run_service_background "API Gateway Microservice" "mvn spring-boot:run" "$BASE_DIR/api-gateway-microservice" "api-gateway"
sleep 10

# Step 3: Start Products microservice
echo "Step 3: Starting Products microservice..."
run_service_background "Products Microservice" "mvn spring-boot:run" "$BASE_DIR/products-microservice" "products"
sleep 10

# Step 4: Start Checkout microservice
echo "Step 4: Starting Checkout microservice..."
run_service_background "Checkout Microservice" "mvn spring-boot:run" "$BASE_DIR/checkout-microservice" "checkout"
sleep 10

# Step 5: Start Cart microservice
echo "Step 5: Starting Cart microservice..."
run_service_background "Cart Microservice" "mvn spring-boot:run" "$BASE_DIR/cart-microservice" "cart"
sleep 10

# Step 6: Start the React UI
echo "Step 6: Starting React UI..."
run_service_background "React UI" "mvn spring-boot:run" "$BASE_DIR/react-ui" "react-ui"

echo ""
echo "=== Bootstrap Complete ===" | tee -a "$LOG_FILE"
echo "Completed at: $(date)" >> "$LOG_FILE"
echo ""
echo "Services should be available at:"
echo "  - Eureka Dashboard: http://localhost:8761/"
echo "  - Marketplace App:  http://localhost:8080/"
echo ""
echo "Check $LOG_FILE for detailed execution log."
echo "Check individual service logs (*.out files) for service output."
echo ""
echo "To stop all services, run: pkill -f 'spring-boot:run'"
