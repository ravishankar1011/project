#!/bin/bash

log_step() {
    echo ""
    echo "----------------------------------------------------"
    echo "$1"
    echo "----------------------------------------------------"
}

# Function to kill processes matching a pattern
# $1: Pattern to search in the command line
# $2: Friendly name of the process for logging
kill_processes_by_pattern() {
    local pattern="$1"
    local process_name="$2"
    local pids

    echo "Attempting to stop $process_name processes matching pattern: '$pattern'..."

    pids=$(pgrep -f "$pattern")

    if [ -n "$pids" ]; then
        echo "Found $process_name PIDs: $pids"
        # Sending SIGTERM (15) for graceful shutdown
        if kill $pids; then
            echo "$process_name processes sent SIGTERM. Waiting a moment..."
            sleep 2 # Give them a moment to shut down
            # Check if they are still alive
            if ps -p $pids > /dev/null; then
                echo "Some $process_name processes may still be running. You might need to use 'kill -9 <PID>' or a more specific pkill."
            else
                echo "$process_name processes successfully terminated."
            fi
        else
            echo "Failed to send SIGTERM to PIDs: $pids. They might have already exited or permissions issue."
        fi
    else
        echo "No running $process_name processes found matching pattern: '$pattern'"
    fi
}

# --- Main Shutdown Sequence ---

# 1. Stop All Android Emulators (Gracefully via ADB first)
log_step "Stopping Android Emulators via ADB"
if command -v adb &> /dev/null; then
    # Get UDIDs of online emulators (lines starting with 'emulator-' and in 'device' state)
    EMULATOR_UDIDS=($(adb devices | awk '$2=="device" && $1 ~ /^emulator-/ {print $1}'))

    if [ ${#EMULATOR_UDIDS[@]} -gt 0 ]; then
        echo "Found running emulators: ${EMULATOR_UDIDS[*]}"
        for udid in "${EMULATOR_UDIDS[@]}"; do
            echo "Sending 'emu kill' command to $udid..."
            if adb -s "$udid" emu kill; then
                echo "Kill command sent successfully to $udid."
            else
                echo "Failed to send kill command to $udid via adb (it might have already shut down or be unresponsive)."
            fi
            sleep 2
        done
        echo "Waiting a few seconds for emulators to shut down gracefully..."
        sleep 5 # Adjust as needed
    else
        echo "No running emulators found connected to ADB."
    fi
else
    echo "Warning: 'adb' command not found. Skipping ADB emulator shutdown."
fi

# 2. Stop Appium Servers
log_step "Stopping Appium Servers"
kill_processes_by_pattern "appium.*" "Appium Server"

# 3. Stop Selenium Grid Hub and Nodes
log_step "Stopping Selenium Grid Hub and Nodes"
kill_processes_by_pattern "java -jar .*selenium-server.*" "Selenium Hub and Nodes"
