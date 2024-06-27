FROM node:20-alpine


WORKDIR /cache
COPY package*.json .
RUN npm install


WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH
ENV NODE_ENV development

COPY . .


EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]