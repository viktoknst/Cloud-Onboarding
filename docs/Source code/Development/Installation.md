This document describes how the project and relevant dependencies, tools, etc. should be installed.

This file is WIP, and not complete.

## Source

First install the source code via `git clone https://github.com/Al1002/cloud_computing.git`

Then, install python requirements, (either in a virtual environment or otherwise)
Ex: `pip install -i requirements.txt`

To make sure installation is successful, try running `pytest test`

To run the project, use `./start-server`

## Dependencies
The app depends on both MongoDB and Docker Engine. 

#### MongoDB
The MongoDB is ran via Docker compose.
No installation necessary.

#### Docker 
The python docker sdk requires an installation of the docker engine.
Its suggested to follow the official installation, however certain follow-up procedures are needed for the project to run.

#### 1. Install docker

Abreviated from the official docker docs:

Remove conflicting packages:

`for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done`


This will download the latest version of Docker from the Ubuntu archives, unpack it, and then install it on your system:
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

#### 2. Post install

You can then start the service with `systemctl`:

`sudo systemctl enable --now docker`
(Note: this also enables it on startup)

However, docker will throw wierd issues if only this is done. Ex:

`docker hello-world`

will return an error. This is because, by default, docker engine only allows users in the docker group. This is true for the app as well: it can not be ran without `sudo`.

To add ourselves to the docker group, use:

`usermod -aG docker $USER`

This will remove the need to use sudo for docker. This is true globally, so keep this in mind.
