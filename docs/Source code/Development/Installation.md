This document describes how the project and relevant dependencies, tools, etc. should be installed.

This file is WIP, and not complete.

## Dependencies
The app depends on both MongoDB and Docker Engine. 

#### MongoDB
1. Follow the official installation instructions at https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition
2. Ensure the mongo server is running. The app makes use of cob_db as its name for mongo database.

#### Docker 
The python docker sdk requires an installation of the docker engine.
While the official installation instructions can be followed, it is suggested to use the following instead

`sudo apt install docker.io`

This will download the latest version of Docker from the Ubuntu archives, unpack it, and then install it on your system.

You can then start the service with `systemctl`:

`sudo systemctl enable --now docker`
(Note: this also enables it on startup)

However, docker will throw wierd issues if only this is done. Ex:

`docker hello-world`

will return an error. This is because, by default, docker engine only allows users in the docker group. This is true for the app as well: it can not be ran without `sudo`.

To add ourselves to the docker group, use:

`usermod -aG docker $USER`

This will remove the need to use sudo for docker. This is true globally, so keep this in mind.