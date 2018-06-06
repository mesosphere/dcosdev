template = """
{
  "assets": {
    "uris": {
      "jre-tar-gz": "https://downloads.mesosphere.com/java/server-jre-8u162-linux-x64.tar.gz",
      "libmesos-bundle-tar-gz": "https://downloads.mesosphere.com/libmesos-bundle/libmesos-bundle-1.11.0.tar.gz",
      "bootstrap-zip": "http://downloads.mesosphere.com/dcos-commons/artifacts/%(version)s/bootstrap.zip",
      "executor-zip": "http://downloads.mesosphere.com/dcos-commons/artifacts/%(version)s/executor.zip",
      "scheduler-zip": "https://s3-us-west-1.amazonaws.com/mbgl-bucket/sdk/%(version)s/operator-scheduler.zip",
      "svc": "http://minio.marathon.l4lb.thisdcos.directory:9000/artifacts/%(template)s/svc.yml"
    }
  },
  "images": {
    "icon-small": "https://github.com/dcos/dcos-ui/blob/master/plugins/services/src/img/icon-service-default-small.png?raw=true",
    "icon-medium": "https://github.com/dcos/dcos-ui/blob/master/plugins/services/src/img/icon-service-default-medium.png?raw=true",
    "icon-large": "https://github.com/dcos/dcos-ui/blob/master/plugins/services/src/img/icon-service-default-large.png?raw=true"
  },
  "cli":{
    "binaries":{
      "darwin":{
        "x86-64":{
          "contentHash":[ { "algo":"sha256", "value":"%(cli-darwin)s" } ],
          "kind":"executable",
          "url":"https://downloads.mesosphere.com/dcos-commons/artifacts/%(version)s/dcos-service-cli-darwin"
        }
      },
      "linux":{
        "x86-64":{
          "contentHash":[ { "algo":"sha256", "value":"%(cli-linux)s" } ],
          "kind":"executable",
          "url":"https://downloads.mesosphere.com/dcos-commons/artifacts/%(version)s/dcos-service-cli-linux"
        }
      },
      "windows":{
        "x86-64":{
          "contentHash":[ { "algo":"sha256", "value":"%(cli-win)s" } ],
          "kind":"executable",
          "url":"https://downloads.mesosphere.com/dcos-commons/artifacts/%(version)s/dcos-service-cli.exe"
        }
      }
    }
  }
}
"""
