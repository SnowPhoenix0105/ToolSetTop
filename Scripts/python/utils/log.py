from python.utils.path import Path, pcat
import logging
import time
import sys

class ShortLevelNameFormatter(logging.Formatter):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        tmp = {
            "DEBUG": "DBG",
            "INFO": "INF",
            "WARNING": "WAR",
            "CRITICAL": "ERR"
        }
        self.levelname_trans = dict({v:v for v in tmp.values()}, **tmp)

    def format(self, record: logging.LogRecord) -> str:
        record.shortlevelname = self.levelname_trans[record.levelname]
        return super().format(record)

def config_logging(file, console_level: int=logging.INFO, file_level: int=logging.DEBUG):
    t = time.strftime("%Y_%m_%d", time.localtime(time.time()))

    file_handler = logging.FileHandler(pcat(Path.SCRIPTS_LOGS, f"{t}.log"), mode='a', encoding="utf8")
    file_handler.setFormatter(ShortLevelNameFormatter('%(asctime)s [%(shortlevelname)s] %(module)s.%(lineno)d %(name)s:\t%(message)s'))
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ShortLevelNameFormatter(
        '[%(asctime)s %(shortlevelname)s] %(message)s',
        datefmt="%Y/%m/%d %H:%M:%S"))
    console_handler.setLevel(console_level)

    logging.basicConfig(
        level=0,
        handlers=[file_handler, console_handler],
        )
    
    logging.info(f"running {file}")

if __name__ == '__main__':
    config_logging(__file__, logging.WARNING, logging.DEBUG)
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.critical("critical")