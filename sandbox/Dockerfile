FROM node:18.3.0-alpine3.14

ENV npm_config_cache=/home/node/app/.npm

WORKDIR /app

COPY package*.json ./

RUN npm install --only=production

COPY src ./src
RUN chmod -R a+x /app

USER node

EXPOSE 9000

CMD ["npm", "run", "start"]
