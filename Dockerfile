# Use official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port for Koyeb deployment (not required for Telegram bot but useful for debugging)
EXPOSE 80

# Run the Python bot
CMD ["python", "telegram_bot.py"]
