# Base image
FROM ubuntu:20.04

# Metadata
LABEL maintainer="mobay@rupaya.io"

# Environment variables
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /shared

# Install required packages and dependencies
RUN apt-get update && \
    apt-get --no-install-recommends -yq install \
    git-core \
    build-essential \
    ruby \
    sudo \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a directory and clone gitian-builder
RUN mkdir /home/ubuntu/ && \
    git clone https://github.com/rupaya-project/gitian-builder /shared/gitian-builder && \
    chmod -R 775 /shared/gitian-builder/target-bin/

# Download MacOSX10.14.sdk.tar.gz
RUN mkdir /shared/gitian-builder/inputs/ && \
    wget https://bitcoincore.org/depends-sources/sdks/Xcode-11.3.1-11C505-extracted-SDK-with-libcxx-headers.tar.gz -O /shared/gitian-builder/inputs/Xcode-11.3.1-11C505-extracted-SDK-with-libcxx-headers.tar.gz

# Set the user to root and specify the command to run when the container starts
USER root
CMD ["/bin/bash", "-c", "/shared/gitian-builder/bin/gbuild --skip-image --commit rupaya=$TAG_OR_BRANCH --url rupaya=$ORG_PROJECT $PLATFORM_YML"]
ENTRYPOINT ["sudo"]
