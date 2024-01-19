# MongoDB Docker Container Setup

This README provides instructions on how to install Docker, set up a MongoDB container, run it, and expose specific ports for accessing the MongoDB database.

## Prerequisites

Before proceeding, ensure that Docker is installed on your system. If Docker is not installed, follow the steps in the 'Installing Docker' section.

## Installing Docker

### For Windows and macOS:

1. Download Docker Desktop from the [Docker official website](https://www.docker.com/products/docker-desktop).
2. Run the installer and follow the on-screen instructions.
3. After installation, launch Docker Desktop.

### For Ubuntu:

1. Update your package index: `sudo apt-get update`.
2. Install packages to allow `apt` to use a repository over HTTPS:
   ```
   sudo apt-get install \
     apt-transport-https \
     ca-certificates \
     curl \
     gnupg-agent \
     software-properties-common
   ```
3. Add Docker’s official GPG key:
   ```
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   ```
4. Set up the stable repository:
   ```
   sudo add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
   ```
5. Update the apt package index again: `sudo apt-get update`.
6. Install the latest version of Docker Engine and containerd:
   ```
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

## Setting Up a MongoDB Container

1. **Pull the MongoDB Image:**
   Pull the latest MongoDB image from Docker Hub:
   ```
   docker pull mongo
   ```

2. **Run the MongoDB Container:**
   Run a MongoDB container and expose the desired ports. Replace `YOUR_CONTAINER_NAME` with your preferred container name, and `YOUR_PORT` with the port number you want to expose (default MongoDB port is 27017):
   ```
   docker run --name YOUR_CONTAINER_NAME -p YOUR_PORT:27017 -d mongo
   ```
   This command will start a MongoDB container in detached mode.

3. **Verify Container Status:**
   To ensure the container is running, use:
   ```
   docker ps
   ```
   Look for `YOUR_CONTAINER_NAME` in the list to confirm it's running.

## Accessing MongoDB

With the MongoDB container running and the port exposed, you can connect to the MongoDB database using any MongoDB client, specifying `localhost` and `YOUR_PORT` as the connection parameters.

For example, to connect via the MongoDB shell, you would use:
```
mongo --host localhost --port YOUR_PORT
```

## Stopping the MongoDB Container

To stop the running container, use the command:
```
docker stop YOUR_CONTAINER_NAME
```

## Starting the MongoDB Container

If the container is stopped and you want to start it again, use:
```
docker start YOUR_CONTAINER_NAME
```

## Additional Information

- To persist data, consider using Docker volumes.
- Always ensure to secure your MongoDB instance, especially when exposing it to public networks.
- Consult Docker and MongoDB documentation for more advanced configurations and usage.

## Conclusion

This guide covers the basic setup of a MongoDB container using Docker. For more advanced configurations, refer to the official Docker and MongoDB documentation.