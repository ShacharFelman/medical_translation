@echo off
docker compose -f docker-compose.dev.yml --env-file .env.development up --build
docker image prune -f
