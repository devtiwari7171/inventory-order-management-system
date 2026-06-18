# Multi-stage: build with Node, serve with nginx.
FROM node:20-alpine AS build
WORKDIR /app

# Accept the API URL at build time so it's baked into the bundle.
ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL

COPY package.json ./
RUN npm install --no-audit --no-fund

COPY . .
RUN npm run build

# ---- Runtime stage ----
FROM nginx:1.27-alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
