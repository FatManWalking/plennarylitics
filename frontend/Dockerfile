FROM node:17-slim as builder

WORKDIR /app

COPY package.json ./
RUN rm -rf node_modules
RUN rm -rf build

COPY . .

RUN npm install
RUN npm run build

FROM node:17-slim as runner

WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./package.json

RUN npm install --production

EXPOSE 3000
ENTRYPOINT ["npm", "run", "start"]