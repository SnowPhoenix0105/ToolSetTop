from python.utils.path import Path, pcat
import logging
import time
import sys

def config_logging(file, console_level: int=logging.INFO, file_level: int=logging.DEBUG):
    _logger_trans = {
            "DEBUG": "DBG",
            "INFO": "INF",
            "WARNING": "WAR",
            "CRITICAL": "ERR"
        }
    _old_factory = logging.getLogRecordFactory()
    def factory(name, level, fn, lno, msg, args, exc_info, func=None, sinfo=None, **kwargs)->logging.LogRecord:
        record = _old_factory(name, level, fn, lno, msg, args, exc_info, func, sinfo, **kwargs)
        record.shortlevelname = _logger_trans[record.levelname]
        return record
    logging.setLogRecordFactory(factory)

    t = time.strftime("%Y_%m_%d", time.localtime(time.time()))
    file_handler = logging.FileHandler(pcat(Path.SCRIPTS_DATA_LOGS, f"{t}.log"), mode='a', encoding="utf8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(shortlevelname)s] %(module)s.%(lineno)d %(name)s:\t%(message)s'
        ))
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s %(shortlevelname)s] %(message)s',
        datefmt="%Y/%m/%d %H:%M:%S"
        ))
    console_handler.setLevel(console_level)

    logging.basicConfig(
        level=min(console_level, file_level),
        handlers=[file_handler, console_handler],
        )
    
    logging.info(f"starting with file: {file}")

if __name__ == '__main__':
    config_logging(__file__, logging.WARNING, logging.DEBUG)
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.critical("critical")

    logger = logging.getLogger(__name__)
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.critical("critical")