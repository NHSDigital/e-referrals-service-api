FROM node:21.6.0-alpine

WORKDIR /app

COPY package*.json ./

ENV npm_config_cache ./.npm
RUN npm install --only=production


COPY src ./src
RUN chmod -R a+x /app

USER nobody

EXPOSE 9000

CMD ["npm", "run", "start"]
