# dcosdev

The *dcosdev* cli provides the one convenient entrypoint for developing operator services (sdk services) or basic service (marathon services).


Start with cloning the `dcosdev` repository.
```
git clone https://github.com/realmbgl/dcosdev.git
cd dcosdev
```


## setup the asset repository

`dcosdev` uses `minio` as its asset repository.

Use the following two commands to install the `minio` service and to make it available via the dc/os public agent.

```
dcos package install marathon-lb --yes
dcos marathon app add misc/minio.json
```

In your browser enter the following address.
```
http://<public-agent-ip>:9000
```


The `minio` credentials are minio / minio123.

Create a bucket named *artifacts* and set its policy to *Read*.


## install

**Note:** Currently `dcosdev` has only been tested with python2 !

Install the `dcosdev` cli.
```
python setup.py install
```


## developer guide

In your workspace create a project folder for your new service.
```
mkdir myservice
cd myservice
```

**Note:** All `dcosdev` cli commands have to run from the root of your project folder.

Here the help output for `dcosdev`.
```
dcosdev -h

dcos service development tools.

Usage:
  dcosdev operator new <name> <sdk-version>
  dcosdev basic new <name>
  dcosdev up
  dcosdev test
  dcosdev release <package-version> <release-version> <s3-bucket> [--universe=<universe>]
  dcosdev operator add java
  dcosdev operator build java
  dcosdev operator upgrade <new-sdk-version>
  dcosdev (-h | --help)
  dcosdev --version

Options:
  -h --help                Show this screen.
  --version                Show version.
  --universe=<universe>    Path to a clone of https://github.com/mesosphere/universe
```

Before you continue make sure you have the *MINIO_HOST* environment variable set.
```
export MINIO_HOST=<public-agent-ip>
```

`dcosdev` gives you the choice to create an operator services (sdk services) or basic services (marathon services).


### operator services, aka sdk service

#### dcosdev operator new

Creating a new operator service.
```
dcosdev operator new myservice 0.42.1
```

Your myservice project will now have the following folder file structure.
```
myservice
 |- svc.yml
 |- universe
     |- package.json
     |- marathon.json.mustache
     |- config.json
     |- resource.json
```

#### configuration templates

If you use configuration templates in the svc then they live in the same folder as the svc.yml file.
```
myservice
 |- svc.yml
 |- myconfiguration.yml
 |- universe
     |- package.json
     |- marathon.json.mustache
     |- config.json
     |- resource.json
```

#### custom scheduler

Use the following command to add gradle and java resources to your project for custom scheduler development.
```
dcosdev operator add java
```

Your myservice project will now have the following folder file structure.
```
myservice
 |- svc.yml
 |- java
 |   |- build.gradle
 |   |- settings.gradle
 |   |- src
 |   |   |- /main/java/com/mesosphere/sdk/engine/scheduler/Main.java
 |- universe
     |- package.json
     |- marathon.json.mustache
     |- config.json
     |- resource.json
```

You build your custom scheduler using the following command.
```
dcosdev operator build java
```


### basic service, aka marathon services

Creating a new basic service.
```
dcosdev basic new myservice
```

Your myservice project will now have the following folder file structure.
```
myservice
 |- cmd.sh
 |- universe
     |- package.json
     |- marathon.json.mustache
     |- config.json
     |- resource.json
```

### dcosdev up

You upload your service assets to the asset repository using the following command. This is the same command for operator and basic services.

```
dcosdev up
```

You will see the following output, showing you the dcos cli commands to take it from here.

```
after 1st up: dcos package repo add myservice-repo --index=0 http://<public-agent-ip>:9000/artifacts/myservice/myservice-repo.json

dcos package install myservice --yes

dcos package uninstall myservice

dcos package repo remove myservice-repo
```

### dcosdev release

Clone the Mesosphere Universe repo to your local file system, and create a branch.

```
git clone https://github.com/mesosphere/universe.git
cd universe
git checkout -b myservice
```

If this is the 1st release of myservice, then you will have to create the *myservice* folder, i.e. *repo/packages/M/myservice* before using the release command. If its not the 1st release check the folder number of the last release in the *myservice* folder. The release version number to use next will have to be greater then the previous one.

Change back to your *myservice* project folder.

Use the *dcosdev release ...* command to upload the release artifacts to s3, and to add a new folder with universe files to the myservice universe branch.

```
dcosdev release 0.1.0-1.0.0 0 <s3-bucket> --universe=<Path to a clone of https://github.com/mesosphere/universe >
```

Change back to your local universe. Commit the changes, push the branch, and and on github create a pull request.
```
...
git push origin myservice
...
```
