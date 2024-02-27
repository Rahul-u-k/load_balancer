# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Install Flask
RUN pip install flask

# Copy the entire contents of the confirmation_page directory into the container at /app
COPY . .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run confirmation_page.py when the container launches
CMD ["python", "confirmation_page.py"]
