#!/bin/bash

# NewsAgent - Weekly Cron Setup Script
# This script helps you set up a weekly cron job for your news digest

echo "=========================================="
echo "NewsAgent Weekly Automation Setup"
echo "=========================================="
echo ""

# Get the current directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"

echo "Project directory: $SCRIPT_DIR"
echo "Python path: $PYTHON_PATH"
echo ""

# Verify python exists
if [ ! -f "$PYTHON_PATH" ]; then
    echo "ERROR: Virtual environment not found at $PYTHON_PATH"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

echo "Choose when you want to receive your weekly digest:"
echo ""
echo "1) Monday at 7:00 AM"
echo "2) Monday at 9:00 AM"
echo "3) Friday at 7:00 AM"
echo "4) Friday at 6:00 PM"
echo "5) Custom (you specify)"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        CRON_TIME="0 7 * * 1"
        DESCRIPTION="Every Monday at 7:00 AM"
        ;;
    2)
        CRON_TIME="0 9 * * 1"
        DESCRIPTION="Every Monday at 9:00 AM"
        ;;
    3)
        CRON_TIME="0 7 * * 5"
        DESCRIPTION="Every Friday at 7:00 AM"
        ;;
    4)
        CRON_TIME="0 18 * * 5"
        DESCRIPTION="Every Friday at 6:00 PM"
        ;;
    5)
        echo ""
        read -p "Enter hour (0-23): " hour
        read -p "Enter minute (0-59): " minute
        echo "Days: 0=Sunday, 1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday, 6=Saturday"
        read -p "Enter day of week (0-6): " day
        CRON_TIME="$minute $hour * * $day"
        DESCRIPTION="Custom schedule"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Your cron job will run: $DESCRIPTION"
echo "=========================================="
echo ""
echo "The following cron job will be added:"
echo ""
echo "$CRON_TIME cd $SCRIPT_DIR && $PYTHON_PATH $SCRIPT_DIR/main.py >> $SCRIPT_DIR/newsagent.log 2>&1"
echo ""
read -p "Do you want to add this cron job? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Aborted."
    exit 0
fi

# Add the cron job
(crontab -l 2>/dev/null; echo "$CRON_TIME cd $SCRIPT_DIR && $PYTHON_PATH $SCRIPT_DIR/main.py >> $SCRIPT_DIR/newsagent.log 2>&1") | crontab -

echo ""
echo "✓ Cron job added successfully!"
echo ""
echo "To view your cron jobs: crontab -l"
echo "To remove this cron job: crontab -e (then delete the line)"
echo "To view logs: tail -f $SCRIPT_DIR/newsagent.log"
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
