## COB
Developer oriented cloud computing web service that can work with different languages.

The project is a service similar to [AWS lambda](https://en.wikipedia.org/wiki/AWS_Lambda) and other server-less providers.

An MVP/demo exists at [this repository](https://github.com/Al1002/cob)

### User stories
Im a computer science student and want to develop my projects in a separate environment, because i lack the hardware to run it on my own device. To do this, the remote environment must support the dependencies i need

Im a data scientist and want to process a large amount of data and extract information from it. To do this, i need a service which can process my load, tell me how much time and resources (money) it will take, and is responsive while its operating.

Im a web developer and want to build a service with auto scaling. To do this, i need to be able to control how much resources my app is able to use.

### Features
- The user has the ability to create and alter user profiles
- The user can get information about their account
- The user can create and alter projects, privately held by their account
- The user can get information about said instances
* The user can create and manage running instances of their projects

### ==Functional requirements==
==MUST - The ability to CRUD user profiles.==

==SHOULD - The ability to CRUD and execute projects in different languages (provided by the service instance), with said projects being owned by different users.==

==MUST - The ability to observe, stop, get results from, specific execution instances.==
