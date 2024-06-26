try {
    docker-compose -f docker-compose.test.yml up --build
}
finally {
    docker image prune -f
}