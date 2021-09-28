from python.utils.log import config_logging
import logging
import subprocess
import shlex
import threading

class CommandExecutionException(Exception):
    def __init__(self, command: str, exit_code: int) -> None:
        super().__init__(f"command executed fail with exit-code={exit_code}: {command}")

_logger = logging.getLogger(__name__)

class TextReadLineThread(threading.Thread):
    def __init__(self, readline, callback, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.readline = readline
        self.callback = callback

    def run(self):
        for line in iter(self.readline, ""):
            if len(line) == 0:
                break
            self.callback(line)


def cmd_exec(command: str, ensure_success: bool=True) -> int:
    _logger.info("executing command: {}".format(command))

    cmd = command # shlex.split(command)

    # _logger.debug(f"cmd={cmd}")

    process = subprocess.Popen(
        cmd,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )

    _logger.debug("started command")

    def log_warp(func):
        def _wrapper(line: str):
            return func("\t" + line.strip())
        return _wrapper

    read_stdout = TextReadLineThread(process.stdout.readline, log_warp(_logger.info))
    read_stderr = TextReadLineThread(process.stderr.readline, log_warp(_logger.warning))
    read_stdout.start()
    read_stderr.start()

    read_stdout.join()
    _logger.debug("stdout reading finish")
    read_stderr.join()
    _logger.debug("stderr reading finish")
    ret = process.wait()
    _logger.debug("process finish")

    _logger.info("executed command with exit-code={}".format(ret))
    if ensure_success and ret != 0:
        raise CommandExecutionException(command=command, exit_code=ret)
    return ret

if __name__ == '__main__':
    config_logging(__file__, logging.DEBUG)
    cmd_exec("ping 127.0.0.1", ensure_success=False)