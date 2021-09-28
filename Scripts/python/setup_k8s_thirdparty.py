

from python.utils.cmd_exec import cmd_exec
import json
import logging
from python.utils.path import Path, pcat
from logging import DEBUG
from python.utils.log import config_logging

_logger = logging.getLogger(__name__)

def setup_k8s_thirdparty():
    list_path = Path.SCRIPTS_CONFIG_K8S_THIRD_PARTY_LIST
    _logger.debug(f"using thrid-party list at path: {list_path}")
    with open(list_path, 'r', encoding='utf8') as f:
        third_party_list = json.load(f)
    for third_party_package in third_party_list:
        name = third_party_package["name"]
        cmd = third_party_package["cmd"]
        desc = third_party_package["desc"]
        _logger.info(f"deploying {name}: {desc}")
        cmd_exec(cmd)


if __name__ == '__main__':
    config_logging(__file__, console_level=logging.INFO)
    setup_k8s_thirdparty()
