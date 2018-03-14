import logging


class LoggingConfig:
    log_string_format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'

    def __init__(self):
        LoggingConfig.setup_stream_logging()
        logging.getLogger('').setLevel(logging.INFO)

    @staticmethod
    def setup_stream_logging():
        strhdlr = logging.StreamHandler()
        strhdlr.setLevel(logging.DEBUG)
        logging.basicConfig(format=LoggingConfig.log_string_format, level=logging.INFO, handlers=[strhdlr])
        logging.getLogger('').log(logging.INFO, "Logging file startup")

