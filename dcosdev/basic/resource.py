template = """
{
  "assets": {
    "uris": {
      "cmd": "http://minio.marathon.l4lb.thisdcos.directory:9000/artifacts/%(template)s/cmd.sh"
    }
  },
  "images": {
    "icon-small": "https://github.com/dcos/dcos-ui/blob/master/plugins/services/src/img/icon-service-default-small.png?raw=true",
    "icon-medium": "https://github.com/dcos/dcos-ui/blob/master/plugins/services/src/img/icon-service-default-medium.png?raw=true",
    "icon-large": "https://github.com/dcos/dcos-ui/blob/master/plugins/services/src/img/icon-service-default-large.png?raw=true"
  }
}
"""
