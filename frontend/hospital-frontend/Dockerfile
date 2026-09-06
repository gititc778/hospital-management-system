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
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
