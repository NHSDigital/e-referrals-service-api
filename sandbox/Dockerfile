FROM node:18.2.0-alpine3.14

WORKDIR /app

COPY package*.json ./

RUN npm install --only=production

COPY src ./src
RUN chmod -R a+x /app

USER nobody

EXPOSE 9000

CMD ["npm", "run", "start"]
