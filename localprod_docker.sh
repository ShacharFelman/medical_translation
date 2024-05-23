docker kill meditranslate
docker build -f Dockerfile -t flask-react:latest .   
docker run -d --rm --name meditranslate --env-file ./.env.localprod -e "PORT=8765" -p 8007:8765 flask-react:latest

