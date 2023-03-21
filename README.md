# Rupaya Gitian Builder

This repository contains scripts and Dockerfiles for building Gitian binaries for the Rupaya cryptocurrency project. Gitian is a deterministic build process that ensures the binaries are built from a specific set of source code and dependencies, which increases their trustworthiness and security. The scripts and Dockerfiles in this repository automate the Gitian build process for different platforms and architectures, making it easier for developers to build and verify the Rupaya binaries.

## Requirements

To use this repository, you need to have the following software installed:

- Docker
- Git
- Python 3

## Usage

To use the Gitian builder, follow these steps:

1. Clone this repository:

git clone https://github.com/your-username/rupaya-gitian-builder.git

2. Navigate to the `rupaya-gitian-builder` directory:

`cd rupaya-gitian-builder`

3. Modify the environment variables in the `Dockerfile` as needed. For example, you can change the default branch or tag to build, or add/remove platforms to build.

4. Run the Python script to select a tag to build and specify the platforms:

`python3 build.py rupaya-project/rupaya osx win`


Replace `rupaya-project/rupaya` with the GitHub organization and project name, and `osx win` with the platforms you want to build.

5. The Python script will prompt you to select a tag to build from a list of tags fetched from GitHub, and then it will build the binaries for the specified platforms using the Gitian builder and Docker.

6. Once the build is complete, the binaries will be available in the `result` directory.

## License

This repository is licensed under the Unlicense
