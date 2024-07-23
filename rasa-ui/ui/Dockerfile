# Use an official Nginx image as the base image
FROM nginx:latest

# Remove the default Nginx welcome page
RUN rm -f /usr/share/nginx/html/index.html

# Copy your chatbot's UI files into the default Nginx web server location
COPY ./ /usr/share/nginx/html/

# Expose port 80 for HTTP
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
