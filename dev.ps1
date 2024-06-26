try {
    docker compose -f docker-compose.dev.yml --env-file .env.development up --build
}
finally {
    docker image prune -f
}