# !/bin/bash

# Define variables and paths
DETECT_FOLDER="/home/mariano/workspace/tesis/RaspberryPiDetect"
APP_FOLDER="/home/mariano/workspace/tesis/RaspberryPiDetect/App"
LOG_FILE="/home/mariano/workspace/tesis/log/run.log"


# Initialize log file with a timestamp
echo "Script started at $(date)" | tee -a "$LOG_FILE" 2>&1

# Check if the detect folder exists
if [ ! -d "$DETECT_FOLDER" ]; then
    echo "Error: Detect folder not found." >> "$LOG_FILE"
    exit 1
else
    echo "Detect folder found."
fi

# Activate virtual environment
source "$DETECT_FOLDER/bin/activate" >> "$LOG_FILE" 2>&1

# Check if activation was successful
if [ $? -ne 0 ]; then
    echo "Error: Virtual environment activation failed." >> "$LOG_FILE"
    exit 1
else
    echo "Virtual env activated."
fi

# Go to App folder
cd "$APP_FOLDER" >> "$LOG_FILE" 2>&1

# Check if the App folder exists
if [ $? -ne 0 ]; then
    echo "Error: App folder not found." >> "$LOG_FILE"
    exit 1
else
    echo "App folder found."
fi

echo "Executing app..."
# Run the app and capture output
python app_2.py >> "$LOG_FILE"

# Check if the app ran successfully
if [ $? -ne 0 ]; then
    echo "Error: App execution failed." >> "$LOG_FILE"
    exit 1
else
    echo "App execution OK."
fi

# Script completed successfully
deactivate
echo "Script completed at $(date)" | tee -a "$LOG_FILE" 2>&1