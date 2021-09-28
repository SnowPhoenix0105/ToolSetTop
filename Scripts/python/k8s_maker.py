import os
from python.utils.log import config_logging
from typing import List
from python.utils.path import Path, ensure_and_clear_dir, pcat
import logging
import json

_logger = logging.getLogger(__name__)

class Setting:
    def __init__(self) -> None:
        self.database = "localhost:3306"

    def produce_spring_config(self, yaml: List[str]) -> List[str]:
        return [line.replace("localhost:3306", self.database) 
            for line in yaml]
    
    def report(self, logger: logging.Logger, prefix=""):
        logger.info(f"{prefix}databass={self.database}")

    def to_json(self):
        return json.dumps({
            "database": self.database
        })
    
    @staticmethod
    def of_json(json_str: str):
        ret = Setting()
        try:
            json_dict = json.loads(ret)
            if "database" in json_dict:
                ret.database = json_dict["database"]
        except:
            return ret
        return ret

def make_k8s_configs(setting: Setting, target_dir=None):
    _logger.info("start making k8s config, with settings:")
    setting.report(_logger, '\t')
    if target_dir is None:
        target_dir = pcat(Path.SCRIPTS_DATA, "k8s")
    _logger.info(f"new configs will save at [{target_dir}]")
    ensure_and_clear_dir(target_dir)
    _copy_configs(Path.SCRIPTS_CONFIG_K8S, target_dir)
    _make_cm_for_spring(Path.SCRIPTS_CONFIG_SPRING, target_dir, setting)
    _logger.info("finish making k8s config, with settings:")

def _copy_configs(src: str, dst: str):
    yamls = os.listdir(src)
    _logger.info("copy k8s-config:")
    for yaml in yamls:
        src_file = pcat(src, yaml)
        dst_file = pcat(dst, yaml)
        _logger.info(f"\t[{src_file}] => [{dst_file}]")
        with open(src_file, 'r', encoding='utf8') as f:
            content = f.readlines()
        with open(dst_file, 'w', encoding='utf8') as f:
            f.writelines(content)
    _logger.info("copy k8s-config finish")
        

def _application_to_cm(name: str, lines: List[str]) -> str:
    content = "    ".join(lines)
    header = f"""kind: ConfigMap
apiVersion: v1
metadata:
  name: {name}-cm
  namespace: tool-set
data:
  application.yaml: |-
    {content}
    """
    return header + content

def _make_cm_for_spring(src: str, dst: str, setting: Setting):
    yamls = os.listdir(src)
    _logger.info("transform from spring-config to k8s-config:")
    for yaml in yamls:
        name = yaml[:-len(".yaml")]
        src_file = pcat(src, yaml)
        dst_file = pcat(dst, name + "-cm.yaml")
        _logger.info(f"\t[{src_file}] => [{dst_file}]")
        with open(src_file, 'r', encoding='utf8') as f:
            content = f.readlines()
        content = setting.produce_spring_config(content)
        cm = _application_to_cm(name, content)
        with open(dst_file, 'w', encoding='utf8') as f:
            f.write(cm)
    _logger.info("transform from spring-config to k8s-config finish!")


if __name__ == '__main__':
    config_logging(__file__)
    setting = Setting()
    setting.database = "mysql:3306"
    make_k8s_configs(setting)