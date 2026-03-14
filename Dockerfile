# Base image - lightweight Python 3.9
FROM python:3.9-slim
# Set the working directory inside the container
WORKDIR /app
# Copy all project files into the container
COPY . .
# Install all Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Launch the pipeline
CMD ["python","main.py"]