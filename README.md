## COB
Developer oriented cloud computing web service that can work with different languages.

The project is a service similar to [AWS lambda](https://en.wikipedia.org/wiki/AWS_Lambda) and other server-less providers.

An MVP/demo exists at [this repository](https://github.com/Al1002/cob)

#### Features
- The user has the ability to create and alter user profiles
- The user can get information about their account
- The user can create and alter projects, privately held by their account
- The user can get information about said instances
- The user can create and manage running instances of their projects

## Installation

#### Server installation

First install the source code via `git clone https://github.com/Al1002/cloud_computing.git`

Note: To install the server you will need to install the dependencies first.

Then, install python requirements using poetry `poetry install`

Activate poetry using `poetry shell`

To make sure installation is successful, try running `pytest test`

To run the project, use `./start-server`

The app depends on both MongoDB and Docker Engine. 

The MongoDB is ran via Docker compose. No install nescessary.

The python docker sdk requires an installation of the docker engine.
Its suggested to follow the official installation, however certain follow-up procedures are needed for the project to run.

#### 1. Install docker

Abreviated from the official docker docs: https://docs.docker.com/engine/install/ubuntu/

Remove conflicting packages:

`for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done`

Add Docker GPG key:

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

This will download the latest version of Docker from the Ubuntu archives, unpack it, and then install it on your system:

`sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`

#### 2. Post install

You can then start the service with `systemctl`:

`sudo systemctl enable --now docker`
(Note: this also enables it on startup)

However, docker will throw wierd issues if only this is done. Ex:

`docker run hello-world`

will return an error. This is because, by default, docker engine only allows users in the docker group. This is true for the app as well: it can not be ran without `sudo`.

To add ourselves to the docker group, use:

`sudo usermod -aG docker $USER`

This will remove the need to use sudo for docker. This is true globally, so keep this in mind.

#### Client instalation

To connect to an existing server simply download the client script. Inside it contains an API for the server.

## Additional information

Documentation is found at the `docs` directory. 
Developed by https://github.com/Al1002 and https://github.com/viktoknst