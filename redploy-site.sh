#!/bin/bash

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
systemctl daemon-reload
systemctl restart myportfolio.service