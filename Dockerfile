FROM node:14

ENV PORT= \
    NODE_ENV= \
    DB_NAME= \
    DB_HOST= \
    DB_PORT= \
    DB_USER= \
    DB_PASSWORD= 

COPY . /app

WORKDIR /app

RUN npm install

ENTRYPOINT ["node", "./src/index.js"]
