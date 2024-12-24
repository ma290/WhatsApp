# Use official Node.js image as a base
FROM node:16-slim

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy all files
COPY . .

# Expose the port
EXPOSE 3000

# Run the bot
CMD ["npm", "start"]
