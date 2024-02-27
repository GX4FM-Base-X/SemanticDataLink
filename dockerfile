# Define python version
ARG     PY_VERSION=3.11

# Use an official Python runtime as a parent image
FROM    python:${PY_VERSION}-slim
ARG     PY_VERSION

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY    . /app
RUN     ls -la

# Install any needed packages specified in requirements.txt
RUN     pip install --no-cache-dir -r requirements.txt

# patch linkml (for documentation see ./linkml/patch folder's readme)
RUN     rm -r /usr/local/lib/python${PY_VERSION}/site-packages/linkml/generators/shaclgen.py
RUN     rm -r /usr/local/lib/python${PY_VERSION}/site-packages/linkml/generators/owlgen.py
COPY    linkml/patch/ /usr/local/lib/python${PY_VERSION}/site-packages/linkml/generators/
RUN     ls -la /usr/local/lib/python${PY_VERSION}/site-packages/linkml/generators/

# Make port 8501 available to the world outside this container
EXPOSE  8501

# Run streamlit.py when the container launches
CMD     ["streamlit", "run", "SemanticDataLink.py"]
