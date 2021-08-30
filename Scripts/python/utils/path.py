import os
import sys
from typing import Iterable

def pcat(dir: str, *subs: Iterable[str])->str:
    return os.path.join(dir, *subs)

class Path:
    SCRIPTS = os.path.abspath(sys.path[0])
    SCRIPTS_LOGS = pcat(SCRIPTS, "logs")
    SCRIPTS_PEM = pcat(SCRIPTS, "pem")
    SCRIPTS_K8S = pcat(SCRIPTS, "k8s")
    SCRIPTS_K8S_THIRD_PARTY_LIST = pcat(SCRIPTS_K8S, "third_party_list.json")

if __name__ == '__main__':
    print(Path.SCRIPTS)
