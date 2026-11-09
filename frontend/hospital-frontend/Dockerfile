# -------- Build Stage --------
FROM node:14-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies with legacy-peer-deps to avoid conflicts
RUN npm install --legacy-peer-deps

# Copy all source files
COPY . .

# Build Angular app for production
RUN npm run build --prod

# -------- Production Stage --------
FROM nginx:alpine

# Copy Angular build output to Nginx html folder
COPY --from=build /app/dist/hospital-frontend /usr/share/nginx/html

# Copy custom Nginx config for Angular routing
# The image entrypoint renders templates/ into conf.d/default.conf at startup
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Sets NGINX_RESOLVER and K8S_DNS_SUFFIX used by the template
COPY 15-k8s-dns.envsh /docker-entrypoint.d/15-k8s-dns.envsh
RUN sed -i 's/\r$//' /docker-entrypoint.d/15-k8s-dns.envsh && \
    chmod +x /docker-entrypoint.d/15-k8s-dns.envsh

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
