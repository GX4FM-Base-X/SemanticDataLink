# Dockerfile for a Streamlit Application

**Dockerfile can be found in root of this repo!**

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

CMD ls

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit.py when the container launches
CMD ["streamlit", "run", "SemanticDataLink.py"]
```

Replace `SemanticDataLink.py` with the name of your Streamlit application file.

## Instructions

### How to Use the Dockerfile

```markdown
## Dockerizing the Streamlit Application

This application is dockerized for easy deployment and isolation. To get started with Docker, follow the steps below.

### Prerequisites

- Docker installed on your system.

**Building Your Docker Image**

1. Navigate to the directory containing your Streamlit application and the `Dockerfile`.
2. Build your Docker image using the following command. Replace `SemanticDataLink` with the name you wish to give your Docker image:

    ```bash
    docker build -t semanticdatalink .
    ```

**Running Your Streamlit Application in a Docker Container**

- Run the following command to start a Docker container from your image, replacing `yourapp` with the name you gave your Docker image:

    ```bash
    docker run -p 8501:8501 --name semanticdatalink  semanticdatalink
    ```

- Open your web browser and go to `http://localhost:8501` to see your Streamlit application running.

