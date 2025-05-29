#!/bin/bash

# Define the log file
LOG_FILE="kathara_usage.log"

# Function to log CPU and Memory usage for mininet-related processes
log_usage() {
    echo "====================================================================" >> "$LOG_FILE"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - CPU and Memory Usage for Kathara-Related Processes" >> "$LOG_FILE"
    echo "====================================================================" >> "$LOG_FILE"
    
    # Log header
    printf "%-10s %-8s %-8s %-8s %-8s %s\n" "USER" "PID" "%CPU" "%MEM" "VSZ(KB)" "COMMAND" >> "$LOG_FILE"
    echo "--------------------------------------------------------------------" >> "$LOG_FILE"
    
    # Get process information, excluding grep and vscode
    ps aux | grep -E 'kathara|docker' | grep -v -E 'grep|code' | sort -k 3,3nr -k 4,4nr | awk '{printf "%-10s %-8s %-8s %-8s %-8s %s\n", $1, $2, $3, $4, $5, $11}' >> "$LOG_FILE"
    
    echo "--------------------------------------------------------------------" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

# Run log_usage every minute
while true; do
    log_usage
    sleep 1
done
