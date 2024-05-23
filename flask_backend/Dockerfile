FROM python:3.11

WORKDIR /src
COPY requirements.txt /src

# needed for cv2 libary
# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     && rm -rf /var/lib/apt/lists/*

# --mount=type=cache,target= caching the build dependancies 
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

CMD ["python3", "app.py"]
