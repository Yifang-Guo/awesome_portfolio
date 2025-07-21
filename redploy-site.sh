#!/bin/bash

echo "Changing to project directory..."
cd ~/awesome_portfolio

echo "Fetching latest changes from GitHub..."
git checkout main
git fetch
git reset origin/main --hard

echo "Spin containers down to prevent out of memory issues on our VPS instances..."
docker compose -f docker-compose.prod.yml down

echo "Spinup Docker Containers using Docker Compose..."
docker compose -f docker-compose.prod.yml up -d --build