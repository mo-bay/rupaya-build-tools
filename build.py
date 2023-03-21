#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
import time
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

def get_tags(org_project):
    """
    Get the list of tags from GitHub for a specific project.

    Args:
    - org_project: str, GitHub organization and project

    Returns:
    - list of str, tags
    """
    response = requests.get(f"https://api.github.com/repos/{org_project}/tags")
    response.raise_for_status()
    tags = response.json()
    return [tag["name"].split("-")[0] for tag in tags]

def select_tag(tags):
    """
    Prompt the user to select a tag from a list.

    Args:
    - tags: list of str, tags

    Returns:
    - str, selected tag
    """
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

def check_mac(platform):
    """
    Check if required files are present for OSX build.

    Args:
    - platform: str, platform name
    """
    if platform == "osx":
        file_path = Path(DEFAULT_CACHE_DIR) / "Xcode-11.3.1-11C505-extracted-SDK-with-libcxx-headers.tar.gz"
        if not file_path.is_file():
            print(f"{MAGENTA}Xcode file {file_path} does not exist in cache, OSX build not available.{RESET}", file=sys.stderr)
            sys.exit(1)

def build_platform(platform, tag, org_project, docker_image):
    """
    Build a platform for a specific tag using Gitian descriptors.

    Args:
    - platform: str, platform name
    - tag: str, tag to build
    - org_project: str, GitHub organization and project
    - docker_image: str, Docker image name
    """
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

def main():
    """
    Main function to build binaries for different platforms using Gitian descriptors.
    """
    parser = argparse.ArgumentParser(description="Build binaries for different platforms using Gitian descriptors")
    parser.add_argument("org_project", metavar="ORG/PROJECT", nargs="?", default=DEFAULT_ORG_PROJECT, help="GitHub organization and project (default: rupaya-project/rupaya)")
    parser.add_argument("platforms", metavar="PLATFORM", nargs="*", default=DEFAULT_PLATFORMS, help="Platforms to build (default: osx win linux)")
    args = parser.parse_args()

    org_project = args.org_project
    platforms = args.platforms

    tags = get_tags(org_project)
    if not tags:
        print(f"{MAGENTA}No tags found for {org_project}, exiting.{RESET}", file=sys.stderr)
        sys.exit(1)

    if not platforms:
        platforms = DEFAULT_PLATFORMS

    for platform in platforms:
        if platform not in DEFAULT_PLATFORMS:
            print(f"{MAGENTA}Invalid platform: {platform}, skipping.{RESET}", file=sys.stderr)
            continue

        tag = select_tag(tags)
        build_platform(platform, tag, org_project, DEFAULT_DOCKER_IMAGE)
