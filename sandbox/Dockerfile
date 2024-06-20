FROM node:22.3.0-alpine

ENV npm_config_cache /home/node/app/.npm

WORKDIR /app

COPY package*.json ./

RUN npm install --only=production

COPY src ./src
RUN chmod -R a+x /app

USER node

EXPOSE 9000

CMD ["npm", "run", "start"]
