import os
import sys
from typing import Iterable
import shutil
import logging

_logger = logging.getLogger(__name__)

def pcat(dir: str, *subs: Iterable[str])->str:
    return os.path.join(dir, *subs)

def ensure_and_clear_dir(path: str):
    if path == "/":
        raise Exception("trying to clear root dir")
    if os.path.exists(path):
        shutil.rmtree(path)
        _logger.info(f"clean up dir: {os.path.abspath(path)}")
    else:
        _logger.info(f"create dir: {os.path.abspath(path)}")
    os.mkdir(path)

class Path:
    SCRIPTS = os.path.abspath(sys.path[0])
    SCRIPTS_DATA = pcat(SCRIPTS, "data")
    SCRIPTS_DATA_LOGS = pcat(SCRIPTS_DATA, "logs")
    SCRIPTS_DATA_PEM = pcat(SCRIPTS_DATA, "pem")
    SCRIPTS_DATA_SAVE = pcat(SCRIPTS_DATA, "save")
    SCRIPTS_DATA_TMP = pcat(SCRIPTS_DATA, "tmp")
    SCRIPTS_CONFIG = pcat(SCRIPTS, "config")
    SCRIPTS_CONFIG_SPRING = pcat(SCRIPTS_CONFIG, "spring")
    SCRIPTS_CONFIG_K8S = pcat(SCRIPTS_CONFIG, "k8s")
    SCRIPTS_CONFIG_K8S_THIRD_PARTY_LIST = pcat(SCRIPTS_CONFIG, "k8s_third_party_list.json")
    SCRIPTS_CONFIG_OTHER = pcat(SCRIPTS_CONFIG, "others")

if __name__ == '__main__':
    print(Path.SCRIPTS)
