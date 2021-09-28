import json
import logging
import os
from typing import Set
from python.utils.log import config_logging
from python.utils.path import Path, pcat
from python.setup_k8s_thirdparty import setup_k8s_thirdparty
from python.k8s_maker import Setting, make_k8s_configs
from python.utils.cmd_exec import cmd_exec
from python.rsa_generator import generate as rsa_generate

_logger = logging.getLogger(__name__)
_setting_path = pcat(Path.SCRIPTS_DATA_SAVE, "setting.json")

def _build_setting() -> Setting:
    if os.path.exists(_setting_path):
        with open(_setting_path, 'r', encoding='utf8') as f:
            return Setting.of_json(f.read())
    return Setting()

def _save_setting(setting: Setting):
    with open(_setting_path, 'w', encoding='utf8') as f:
        f.write(setting.to_json())

def _build_secret():
    op = input("是否需要重新生成rsa密钥？（重新生成可能导致大部分服务需要重启）")
    if op.lower() not in {'y', 'yes'}:
        _logger.info("skipping rsa-key Secret generation")
        return
    _logger.info(f"building rsa-secret to [{Path.SCRIPTS_DATA_PEM}]")
    rsa_generate(Path.SCRIPTS_DATA_PEM)
    cmd_exec(
        "kubectl create secret generic rsa-secret" +
        " --namespace=toolset" + 
        " --from-file=" + pcat(Path.SCRIPTS_DATA_PEM, "pub.pem") +
        " --from-file=" + pcat(Path.SCRIPTS_DATA_PEM, "pri.pkcs1.pem") +
        " --from-file=" + pcat(Path.SCRIPTS_DATA_PEM, "pri.pkcs8.pem"))

def _build_encoding_charSet():
    op = input("是否需要重新导入charSet文件？（重复导入可能保存，需删除现有ConfigMap）")
    if op.lower() not in {'y', 'yes'}:
        _logger.info("skipping charSet file ConfigMap generation")
        return
    src_dir = pcat(Path.SCRIPTS_CONFIG_OTHER, "charSet")
    _logger.info(f"building charSet file ConfigMap from {src_dir}")
    cmd_exec(
        "kubectl create configmap encoding-transformer-charset" +
        " --namespace=toolset" + 
        " --from-file=" + pcat(src_dir, "common3500.txt") +
        " --from-file=" + pcat(src_dir, "common7000.txt"))


def _apply_config(path: str):
    yamls = os.listdir(path)
    for yaml in yamls:
        full_path = pcat(path, yaml)
        cmd_exec(f"kubectl apply -f {full_path}")

def _do_deploy(setting: Setting):
    _build_secret()
    _build_encoding_charSet()
    _logger.info("resoving third party k8s modules")
    setup_k8s_thirdparty()
    k8s_file_path = pcat(Path.SCRIPTS_DATA, "k8s")
    _logger.info("build k8s config files")
    make_k8s_configs(setting, k8s_file_path)
    _logger.info("applying k8s configs")
    _apply_config(k8s_file_path)


def start_deploy():
    setting = _build_setting()
    try:
        while True:
            print("当前配置：")
            print(f"\tdatabase:{setting.database}")
            cmd = input("输入需要修改的配置名以开始修改，或输入回车以开始部署工作")
            if (len(cmd) == 0):
                _do_deploy(setting)
                break
            if cmd in {"database", "db", "data"}:
                print(f"database当前值为{setting.database}")
                new_value = input("您希望修改为: ")
                setting.database = new_value
                print(f"修改成功, 当前database={setting.database}")
            else:
                print(f"未知的设定项: {cmd}")
    finally:
        _save_setting(setting)

if __name__ == '__main__':
    config_logging(__file__)
    start_deploy()