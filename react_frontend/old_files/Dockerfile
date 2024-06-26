FROM node:14 AS builder

WORKDIR /cache
COPY package*.json .
RUN npm install


WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_ENV development

COPY . .
