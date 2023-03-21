#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

# Define colors for output
GREEN = "\033[32m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
RESET = "\033[0m"

# Define default values
DEFAULT_ORG_PROJECT = "rupaya-project/rupaya"
DEFAULT_PLATFORMS = ["osx", "win", "linux"]
DEFAULT_DOCKER_IMAGE = "builder"
DEFAULT_CACHE_DIR = "cache"
DEFAULT_RESULT_DIR = "result"

# Define function to get the list of tags from GitHub
def get_tags(org_project):
    response = requests.get(f"https://api.github.com/repos/{org_project}/tags")
    response.raise_for_status()
    tags = response.json()
    return [tag["name"].split("-")[0] for tag in tags]

# Define function to prompt the user to select a tag from a list
def select_tag(tags):
    print("Please select a tag to build:")
    for i, tag in enumerate(tags):
        print(f"{i + 1}. {tag}")
    while True:
        try:
            choice = int(input("> "))
            if 1 <= choice <= len(tags):
                return tags[choice - 1]
        except ValueError:
            pass
        print(f"Invalid choice, please enter a number between 1 and {len(tags)}.")

# Define function to check if required files are present for OSX build
def check_mac(platform):
    if platform == "osx":
        cache_dir = Path(DEFAULT_CACHE_DIR)
        file_path = cache_dir / "Xcode-11.3.1-11C505-extracted-SDK-with-libcxx-headers.tar.gz"
        if not file_path.is_file():
            print(f"{MAGENTA}Xcode file {file_path} does not exist in cache, OSX build not available.{RESET}", file=sys.stderr)
            sys.exit(1)

# Define function to build a platform for a specific tag
def build_platform(platform, tag, org_project, docker_image):
    check_mac(platform)
    sdate = int(time.time())
    print(f"{CYAN}Starting {platform} build of tag: {tag} at: {time.asctime()}{RESET}")
    cmd = [
        "docker",
        "run",
        "--rm",
        "--name",
        f"builder-{sdate}",
        "-v",
        f"{DEFAULT_CACHE_DIR}:/shared/cache:Z",
        "-v",
        f"{DEFAULT_RESULT_DIR}:/shared/result:Z",
        docker_image,
        tag,
        org_project,
        f"../rupaya/contrib/gitian-descriptors/gitian-{platform}.yml",
    ]
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError as e:
        print(f"{MAGENTA}Build failed with error: {e}{RESET}", file=sys.stderr)
        sys.exit(1)

# Define main function
def main():
    parser = argparse.ArgumentParser(description="Build binaries for different platforms using Gitian descriptors")
    parser.add_argument("org_project", metavar="ORG/PROJECT", nargs="?", default=DEFAULT_ORG_PROJECT, help="GitHub organization and project (default: rupaya-project/rupaya)")
    parser.add_argument("platforms", metavar="PLATFORM", nargs="*", default=DEFAULT_PLATFORMS, help="Platforms to build (default: osx win linux)")
    args = parser.parse_args()
