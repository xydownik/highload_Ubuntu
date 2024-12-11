#!/bin/bash
echo "Deploying to staging..."
docker-compose down  # Stops all running containers
docker-compose up -d --build  # Rebuilds and starts the containers
echo "Staging deployed successfully."
