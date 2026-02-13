#!/bin/bash

# NewsAgent - Daily Cron Setup Script
# Sets up daily news digest delivery at 8am

echo "=========================================="
echo "NewsAgent Daily Automation Setup"
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

echo "This will set up a daily digest at 8:00 AM (your Mac's timezone)."
echo ""
echo "⚠️  TIMEZONE NOTE:"
echo "The cron job will run at 8am in your Mac's current timezone."
echo "If you're in Central Time, make sure your Mac is set to Central timezone."
echo ""

# Check current timezone
CURRENT_TZ=$(date +%Z)
echo "Your Mac's current timezone appears to be: $CURRENT_TZ"
echo ""

read -p "Continue with daily 8am setup? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Aborted."
    exit 0
fi

# Cron time for 8am daily
CRON_TIME="0 8 * * *"
DESCRIPTION="Every day at 8:00 AM"

echo ""
echo "=========================================="
echo "Your cron job will run: $DESCRIPTION"
echo "=========================================="
echo ""
echo "The following cron job will be added:"
echo ""
echo "$CRON_TIME cd $SCRIPT_DIR && $PYTHON_PATH $SCRIPT_DIR/main.py >> $SCRIPT_DIR/newsagent.log 2>&1"
echo ""
read -p "Add this cron job? (y/n): " final_confirm

if [ "$final_confirm" != "y" ]; then
    echo "Aborted."
    exit 0
fi

# Add the cron job
(crontab -l 2>/dev/null; echo "$CRON_TIME cd $SCRIPT_DIR && $PYTHON_PATH $SCRIPT_DIR/main.py >> $SCRIPT_DIR/newsagent.log 2>&1") | crontab -

echo ""
echo "✓ Cron job added successfully!"
echo ""
echo "Your daily news digest will arrive at 8:00 AM every day."
echo ""
echo "Useful commands:"
echo "  View cron jobs:    crontab -l"
echo "  Edit cron jobs:    crontab -e"
echo "  View logs:         tail -f $SCRIPT_DIR/newsagent.log"
echo "  Test manually:     python3 main.py"
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
