#!/usr/bin/env python

"""dcos service development tools.

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

"""
from docopt import docopt
import os, sys, json, base64, time, datetime
from collections import OrderedDict
sys.dont_write_bytecode=True
from minio import Minio
from minio.error import ResponseError
import docker, requests

import oper
import basic


def operator_name():
    with open('universe/package.json', 'r') as f:
         package = json.load(f)
    return package['name']
def sdk_version():
    with open('universe/package.json', 'r') as f:
         package = json.load(f)
    return package['tags'][0]
def sha_values():
    r = requests.get('https://downloads.mesosphere.com/dcos-commons/artifacts/'+sdk_version()+'/SHA256SUMS')
    return {e[1]:e[0] for e in map(lambda e: e.split('  '), str(r.text).split('\n')[:-1])}

def build_repo():
    repository = {'packages': [] }
    packages = repository['packages']

    with open('universe/package.json', 'r') as f:
         package = json.load(f)
    with open('universe/config.json', 'r') as f:
         config = json.load(f, object_pairs_hook=OrderedDict)
    with open('universe/resource.json', 'r') as f:
         resource = json.load(f)
    with open('universe/marathon.json.mustache', 'r') as f:
         s = f.read()
         marathon = base64.b64encode(s%{'time_epoche_ms': str(int(time.time()*1000)), 'time_str': datetime.datetime.utcnow().isoformat()})

    if os.path.exists('java/build/distributions/operator-scheduler.zip'):
         resource['assets']['uris']['scheduler-zip'] = 'http://minio.marathon.l4lb.thisdcos.directory:9000/artifacts/'+operator_name()+'/operator-scheduler.zip'

    package['releaseVersion'] = 100
    package['config'] = config
    package['resource'] = resource
    package['marathon'] = {"v2AppMustacheTemplate": marathon}

    packages.append(package)
    with open('universe/'+operator_name()+'-repo.json', 'w') as file:
         file.write(json.dumps(repository, indent=4))

def upload(artifacts):
    minio_host = os.environ['MINIO_HOST']
    minioClient = Minio(minio_host+':9000', access_key='minio', secret_key='minio123', secure=False)

    for a in artifacts:
        try:
           file_stat = os.stat(a)
           file_data = open(a, 'rb')
           minioClient.put_object('artifacts', operator_name()+'/'+os.path.basename(a), file_data, file_stat.st_size, content_type='application/vnd.dcos.universe.repo+json;charset=utf-8;version=v4')
        except ResponseError as err:
           print(err)

def main():
    args = docopt(__doc__, version='dcosdev 0.0.1')
    print(args)

    if  args['operator'] and args['new']:
        with open('svc.yml', 'w') as file:
             file.write(oper.svc.template%{'template': args['<name>']})

        os.makedirs('universe')
        with open('universe/package.json', 'w') as file:
             file.write(oper.package.template%{'template': args['<name>'],'version': args['<sdk-version>']})
        with open('universe/marathon.json.mustache', 'w') as file:
             file.write(oper.mjm.template)
        with open('universe/config.json', 'w') as file:
             file.write(oper.config.template%{'template': args['<name>']})
        with open('universe/resource.json', 'w') as file:
             d = sha_values()
             file.write(oper.resource.template%{'template': args['<name>'],'version': args['<sdk-version>'], 'cli-darwin': d['dcos-service-cli-darwin'], 'cli-linux': d['dcos-service-cli-linux'], 'cli-win': d['dcos-service-cli.exe']})

    elif args['basic'] and args['new']:
        with open('cmd.sh', 'w') as file:
             file.write(basic.cmd.template%{'template': args['<name>']})

        os.makedirs('universe')
        with open('universe/package.json', 'w') as file:
             file.write(basic.package.template%{'template': args['<name>']})
        with open('universe/marathon.json.mustache', 'w') as file:
             file.write(basic.mjm.template)
        with open('universe/config.json', 'w') as file:
             file.write(basic.config.template%{'template': args['<name>']})
        with open('universe/resource.json', 'w') as file:
             file.write(basic.resource.template%{'template': args['<name>']})

    elif args['up']:
        build_repo()
        artifacts = [f for f in os.listdir('.') if os.path.isfile(f)]
        artifacts.append(str('universe/'+operator_name()+'-repo.json'))
        if os.path.exists('java/build/distributions/operator-scheduler.zip'):
            artifacts.append(str('java/build/distributions/operator-scheduler.zip'))
        print(artifacts)
        upload(artifacts)
        print('\nafter 1st up: dcos package repo add '+operator_name()+'-repo --index=0 http://'+os.environ['MINIO_HOST']+':9000/artifacts/'+operator_name()+'/'+operator_name()+'-repo.json')
        print('\ndcos package install '+operator_name()+' --yes')
        print('\ndcos package uninstall '+operator_name())
        print('\ndcos package repo remove '+operator_name()+'-repo'+'\n')

    elif args['operator'] and args['add'] and args['java']:
        os.makedirs('java/src/main/java/com/mesosphere/sdk/operator/scheduler')
        with open('java/build.gradle', 'w') as file:
             file.write(oper.build_gradle.template%{'version': sdk_version()})
        with open('java/settings.gradle', 'w') as file:
             file.write(oper.settings_gradle.template)
        with open('java/src/main/java/com/mesosphere/sdk/operator/scheduler/Main.java', 'w') as file:
             file.write(oper.main_java.template)

    elif args['operator'] and args['build'] and args['java']:
        print('>>> gradle build ...')
        dockerClient = docker.from_env()
        log = dockerClient.containers.run('gradle:4.8.0-jdk8', 'gradle check distZip', remove=True,
                                    volumes={os.getcwd()+'/java' : {'bind': '/home/gradle/project'}}, working_dir='/home/gradle/project')
        print(log)

    elif args['operator'] and args['upgrade']:
        old_sdk_version = sdk_version()
        print('>>> upgrade from '+old_sdk_version+' to '+args['<new-sdk-version>'])

        with open('universe/package.json', 'r') as f:
             package = f.read().replace(old_sdk_version, args['<new-sdk-version>'])
        with open('universe/package.json', 'w') as f:
             f.write(package)

        with open('universe/resource.json', 'r') as f:
             resource = f.read().replace(old_sdk_version, args['<new-sdk-version>'])
        with open('universe/resource.json', 'w') as f:
             f.write(resource)

        if os.path.exists('java/build.gradle'):
            with open('java/build.gradle', 'r') as f:
                 build_gradle = f.read().replace(old_sdk_version, args['<new-sdk-version>'])
            with open('java/build.gradle', 'w') as f:
                 f.write(build_gradle)


if __name__ == '__main__':
    main()
