# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install Git
RUN apt-get update && apt-get install -y git

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install sentence-transformers from GitHub
RUN pip install git+https://github.com/UKPLab/sentence-transformers.git

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI app and NLPtask
CMD ["bash", "-c", "uvicorn fastapiapp:app --host 0.0.0.0 --port 8000 --reload & python NLPtask.py"]
