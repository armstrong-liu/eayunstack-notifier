import os
import logging
import logging.config
from eayunstack_notifier.config import CONF


class LOGManager(object):
    def __init__(self):
        self.log_file = CONF.get('log', 'file')
        self.log_level = CONF.get('log', 'default')

    def _set_log_path(self):
        # ensure LOG_PATH exists
        if not os.path.exists(os.path.dirname(self.log_file)):
            os.mkdir(os.path.dirname(self.log_file))

    def set_log_conf(self):
        """Log base configure"""
        self._set_log_path()
        dictLogConfig = {
            "version": 1,
            "handlers": {
                "fileHandler": {
                    "class": "logging.FileHandler",
                    "formatter": "myFormatter",
                    "filename": "%s" % self.log_file
                },
                "streamHandler": {
                    "class": "logging.StreamHandler",
                    "formatter": "myFormatter",
                }
            },
            "loggers": {
                "eayunstack_notifier": {
                    "handlers": ["fileHandler", "streamHandler"],
                    "level": "%s" % self.log_level,
                }
            },

            "formatters": {
                "myFormatter": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - "
                              "%(message)s"
                }
            }
        }

        logging.config.dictConfig(dictLogConfig)

        logger_instance = logging.getLogger("eayunstack_notifier")

        return logger_instance


LOGMANAGER = LOGManager()
logger = LOGMANAGER.set_log_conf()
