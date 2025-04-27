# Stage 1: Build Stage
# Use a Node.js base image for building the React app
FROM node:20-alpine as builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
# to install dependencies before copying the rest of the code
COPY package*.json ./

# Install dependencies
RUN npm ci # 'npm ci' is preferred for clean installs in CI/build environments

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# ---

# Stage 2: Serve Stage
# Use a lightweight Nginx image to serve the static files
FROM nginx:alpine

# Copy the built React app files from the builder stage into Nginx's public directory
COPY --from=builder /app/dist /usr/share/nginx/html
# If you used create-react-app, the build directory might be /app/build

# Remove default nginx index page
#RUN rm /etc/nginx/conf.d/default.conf

# Copy a custom Nginx configuration (optional but good practice)
# You would create a file like nginx.conf in your ui/ directory
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose the default Nginx HTTP port
EXPOSE 80

# Command to run Nginx (default command in nginx:alpine base image)
CMD ["nginx", "-g", "daemon off;"]
