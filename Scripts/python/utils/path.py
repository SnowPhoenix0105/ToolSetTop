import os
import sys
from typing import Iterable

def pcat(dir: str, *subs: Iterable[str]):
    return os.path.abspath(os.path.join(dir, *subs))

class Path:
    SCRIPTS = sys.path[0]
    SCRIPTS_LOGS = pcat(SCRIPTS, "logs")
    SCRIPTS_K8S = pcat(SCRIPTS, "k8s")
    SCRIPTS_K8S_THIRD_PARTY_LIST = pcat(SCRIPTS_K8S, "third_party_list.json")

if __name__ == '__main__':
    print(Path.SCRIPTS)
