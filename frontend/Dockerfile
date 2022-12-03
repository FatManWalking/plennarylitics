FROM node:17 as builder

WORKDIR /app

RUN npm install --location=global pnpm

# install dependencies
COPY pnpm-lock.yaml pnpm-workspace.yaml ./
COPY ./frontend/package.json .
RUN pnpm install --filter frontend

# build application
ADD ./frontend frontend
RUN pnpm run --dir frontend build

FROM node:17-alpine

WORKDIR /app
COPY --from=builder /app/frontend .
COPY --from=builder /app/node_modules /app/node_modules

EXPOSE 3000
CMD ["node", "build"]
