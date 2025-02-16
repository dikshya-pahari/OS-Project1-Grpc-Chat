# Use a reliable base image
FROM ubuntu:22.04


WORKDIR /app

# Update and install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev gcc libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create an alias so 'python' refers to 'python3' - bc didn't work in my pc
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copying project files into the container
COPY . /app

RUN python3 -m pip install --upgrade pip

# Installing gRPC dependencies
RUN pip install --no-cache-dir grpcio grpcio-tools grpcio-status grpcio-reflection grpcio-health-checking

#  command to run the test script
CMD ["python3", "run_test_1.py"]
