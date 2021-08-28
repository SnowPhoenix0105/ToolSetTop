本文件夹存放用于运维的脚本文件。

## Python环境

* Python版本： 3.9 以上；
* 运行目录：Scripts（请确保先通过cd指令将当前目录切换至Scripts目录再运行，否则python的import会报错）；
* 库依赖：暂时没有，将来会通过`pip freeze`导出到文件中，可以通过`pip install -r`来安装依赖库；

## k8s第三方依赖

有些操作暂时不知道如何以yaml的格式进行配置，所以将命令保存在[third_party_list.json](k8s/third_party_list.json)中，通过Python脚本[setup_k8s_thirdparty.py](python/setup_k8s_thirdparty.py)来执行。
