# Use an ARM64 ubuntu base image
FROM arm64v8/debian AS builder

# Avoid interaction during package installation
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/KhronosGroup/OpenCL-Headers.git opencl_headers

RUN cp -r opencl_headers/* /usr/local/include

# Install build essential tools and OpenCL headers
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    ocl-icd-libopencl1 \
    ocl-icd-dev \
    opencl-headers \
    vim \
    ocl-icd-opencl-dev \
    pocl-opencl-icd \
    && rm -rf /var/lib/apt/lists/*



# Set working directory
WORKDIR /app

# Copy your source code
COPY . .

RUN gcc opencl_device.cpp -I/usr/local/include -lOpenCL -o opencl_device
# Example Build Command: 
# Link statically against ocl-icd and opencl-headers
# RUN g++ -static main.cpp -lOpenCL -I/usr/include -o my_opencl_app

# CMD ["/bin/bash"]

FROM arm64v8/debian

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ocl-icd-libopencl1 \
    pocl-opencl-icd \
    strace \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/opencl_device /opencl_device

CMD ["/opencl_device"]
