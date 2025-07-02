#!/bin/bash
echo "Killing all existing tmux sessions..."
tmux kill-server 

echo "Changing to project directory..."
cd ~/awesome_portfolio

echo "Fetching latest changes from GitHub..."
git checkout main
git fetch
git reset origin/main --hard

echo "Activating virtual environment and installing dependencies..."
source .venv/bin/activate
pip install -r requirements.txt

echo "Starting Flask server in new tmux session..."
tmux new-session -d -s flask_server "source .venv/bin/activate && flask run --host=0.0.0.0 --port=5000"