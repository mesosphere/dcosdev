template = """
{
  "id": "{{service.name}}",
  "user": "{{service.user}}",
  "instances": {{node.count}},
  "cpus": {{node.cpus}},
  "mem": {{node.mem}},
  "cmd": "env | sort && ./cmd.sh",
  "labels": {
    "DCOS_SERVICE_NAME": "{{service.name}}",
    "DCOS_SERVICE_PORT_INDEX": "0",
    "DCOS_SERVICE_SCHEME": "http"
  },
  {{#service.service_account_secret}}
  "secrets": {
    "serviceCredential": {
      "source": "{{service.service_account_secret}}"
    }
  },
  {{/service.service_account_secret}}
  "env": {
    "PACKAGE_NAME": "{{package-name}}",
    "PACKAGE_VERSION": "{{package-version}}",
    "PACKAGE_BUILD_TIME_EPOCH_MS": "%(time_epoche_ms)s",
    "PACKAGE_BUILD_TIME_STR": "%(time_str)s",
    "SLEEP_DURATION": "{{service.sleep}}"
  },
  "fetch": [
    {"uri": "{{resource.assets.uris.cmd}}", "executable": true}
  ],
  "upgradeStrategy":{
    "minimumHealthCapacity": 0,
    "maximumOverCapacity": 0
  }
}
"""
