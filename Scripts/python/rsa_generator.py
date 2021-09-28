import logging
import os
from python.utils.path import pcat, Path
from python.utils.cmd_exec import cmd_exec
from python.utils.log import config_logging

def generate(target_dir: str):
    # Windows下，openssl似乎还是用/作为文件分隔符，使用\将导致无法正常工作
    pri_pkcs1 = pcat(target_dir, "pri.pkcs1.pem").replace("\\", "/")
    pri_pkcs8 = pcat(target_dir, "pri.pkcs8.pem").replace("\\", "/")
    pub = pcat(target_dir, "pub.pem").replace("\\", "/")

    cmd_exec(f"openssl genrsa -out {pri_pkcs1} 2048")
    cmd_exec(f"openssl rsa -in {pri_pkcs1} -pubout -out {pub}")
    cmd_exec(f"openssl pkcs8 -topk8 -inform PEM -in {pri_pkcs1}"
           + f" -outform PEM -nocrypt -out {pri_pkcs8}")


if __name__ == '__main__':
    config_logging(__name__, logging.DEBUG)
    generate(Path.SCRIPTS_DATA_PEM)