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

## Instalation

#### Server instalation

First install the source code via `git clone https://github.com/Al1002/cloud_computing.git`

Then, install python requirements using poetry
`poetry install`
Activate poetry using `poetry shell`

To make sure installation is successful, try running `pytest test`

To run the project, use `./start-server`

The app depends on both MongoDB and Docker Engine. 

1. Follow the official installation instructions at https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#install-mongodb-community-edition
2. Ensure the mongo server is running. The app makes use of cob_db as its name for mongo database.

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

#### Client instalation

To connect to an existing server simply download the client script. Inside it contains an API for the server.

## Additional information

Documentation is found at the `docs` directory. 
Developed by https://github.com/Al1002 and https://github.com/viktoknst