# dcosdev

First clone this repository.
```
git clone https://github.com/realmbgl/dcosdev.git
cd dcosdev
```

## setup asset repository

dcosdev uses minio as its asset repository.

Use the following two commands to install the minio service and make it available via the public agent.

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

Install the dcosdev tool.
```
python setup.py install
```

## using

In your workspace create a project folder for your new service.
```
mkdir myservice
cd myservice
```

Here teh help output for dcosdev.
```
dcosdev -h
dcos service development tools.

Usage:
  dcosdev new operator <name> <sdk-version>
  dcosdev new basic <name>
  dcosdev up
  dcosdev test
  dcosdev build
  dcosdev release
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

You can create operator services (sdk based), or basic services (marathon).

### dcosdev new operator

Creating a new operator service, i.e. a sdk based service.
```
dcos new operator myservice 0.42.1
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

### dcosdev new basic

Creating a new basic service, i.e. a marathon service.
```
dcos new basic myservice
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

