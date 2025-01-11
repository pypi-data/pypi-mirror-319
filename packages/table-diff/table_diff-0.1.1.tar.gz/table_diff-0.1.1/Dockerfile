FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the project.
RUN pip install -e '.[dev]'

# Set the default command to start a bash shell
CMD ["/bin/bash"]
