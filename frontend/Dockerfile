FROM node:22-slim

WORKDIR /app

COPY package*.json ./
RUN chown node:node /app

USER node

RUN npm ci

COPY --chown=node:node . .

EXPOSE 5173

CMD [ "npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
