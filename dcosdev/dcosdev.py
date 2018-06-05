#!/usr/bin/env python

"""dcos service development tools.

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

"""
from docopt import docopt
import os, sys, json, base64, time, datetime
from collections import OrderedDict
sys.dont_write_bytecode=True
from minio import Minio
from minio.error import ResponseError

import oper
import basic


def operator_name():
    with open('universe/package.json', 'r') as f:
         package = json.load(f)
    return package['name']

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

    if args['new'] and args['operator']:
        with open('svc.yml', 'w') as file:
             file.write(oper.svc.template%{'template': args['<name>']})

        os.makedirs('universe')
        with open('universe/package.json', 'w') as file:
             file.write(oper.package.template%{'template': args['<name>']})
        with open('universe/marathon.json.mustache', 'w') as file:
             file.write(oper.mjm.template)
        with open('universe/config.json', 'w') as file:
             file.write(oper.config.template%{'template': args['<name>']})
        with open('universe/resource.json', 'w') as file:
             file.write(oper.resource.template%{'template': args['<name>'],'version': args['<sdk-version>']})

    if args['new'] and args['basic']:
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
             file.write(basic.resource.template%{'template': args['<name>'],'version': args['<sdk-version>']})

    elif args['up']:
        build_repo()
        artifacts = [f for f in os.listdir('.') if os.path.isfile(f)]
        artifacts.append(str('universe/'+operator_name()+'-repo.json'))
        print(artifacts)
        upload(artifacts)
        print('\nafter 1st up: dcos package repo add '+operator_name()+'-repo --index=0 http://'+os.environ['MINIO_HOST']+':9000/artifacts/'+operator_name()+'/'+operator_name()+'-repo.json')
        print('\ndcos package install '+operator_name()+' --yes')
        print('\ndcos package uninstall '+operator_name())
        print('\ndcos package repo remove '+operator_name()+'-repo'+'\n')


if __name__ == '__main__':
    main()
