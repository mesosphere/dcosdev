# dcosdev

The *dcosdev* cli provides the one convenient entrypoint for deveopering operator services (sdk services) or basic service (marathon services).


Start with cloning the dcosdev repository.
```
git clone https://github.com/realmbgl/dcosdev.git
cd dcosdev
```


## setup the asset repository

dcosdev uses minio as its asset repository.

Use the following two commands to install the minio service and to make it available via the dc/os public agent.

```
dcos package install marathon-lb --yes
dcos marathon app add misc/minio.json
```

In your browser enter the following address.
```
http://<public-agent-ip>:9000
```


The minio credentials are minio / minio123.

Create a bucket named *artifacts* and set its policy to *Read And Write*.


## install

Install the dcosdev cli.
```
python setup.py install
```


## developer guide

In your workspace create a project folder for your new service.
```
mkdir myservice
cd myservice
```

**Note:** All dcosdev cli commands have to run from the root of your project folder.

Here the help output for dcosdev.
```
dcosdev -h

dcos service development tools.

Usage:
  dcosdev operator new <name> <sdk-version>
  dcosdev basic new <name>
  dcosdev up
  dcosdev test
  dcosdev release
  dcosdev operator add java
  dcosdev operator build java
  dcosdev operator upgrade <new-sdk-version>
  dcosdev (-h | --help)
  dcosdev --version

Options:
  -h --help     Show this screen.
  --version     Show version.
```

Before you continue make sure you have the *MINIO_HOST* environment variable set.
```
export MINIO_HOST=<public-agent-ip>
```

dcosdev gives you the choice to create an operator services (sdk services) or basic services (marathon services).


### operator services, aka sdk service

#### dcosdev operator new

Creating a new operator service.
```
dcos operator new myservice 0.42.1
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

#### custom scheduler

Use the following command to add gradle and java resources to your project for custome scheduler development.
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

You build your custome scheduler using the following command.
```
dcosdev operator build java
```


### basic service, aka marathon services

Creating a new basic service.
```
dcos basic new myservice
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

