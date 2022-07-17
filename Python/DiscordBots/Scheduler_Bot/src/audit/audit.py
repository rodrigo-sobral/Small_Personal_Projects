import logging

class LoggerInfo:

    LOG_FILE_PATH = "../logs/infos.log"
    FORMAT = '%(asctime)s - %(channel_name)s - %(levelname)s - FROM %(sender)s TO %(receivers)s WITH %(attachments)s'

    def __init__(self):
        logging.basicConfig(format=self.FORMAT, filename=self.LOG_FILE_PATH, level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

    def logInfo(self, message):
        self.logger.info(message)
        return self.logger
    

class LoggerError:

    LOG_FILE_PATH = "../logs/errors.log"
    FORMAT = '%(asctime)s - %(channel_name)s - %(levelname)s - FROM %(sender)s TO %(receivers)s WITH %(attachments)s'

    def __init__(self):
        logging.basicConfig(format=self.FORMAT, filename=self.LOG_FILE_PATH, level=logging.ERROR)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

    def logError(self, message):
        self.logger.error(message)
        return self.logger
    
    def logWarning(self, message):
        self.logger.warning(message)
        return self.logger

    def logCritical(self, message):
        self.logger.critical(message)
        return self.logger
    

class LoggerDebug:

    LOG_FILE_PATH = "../logs/debugs.log"
    FORMAT = '%(asctime)s - %(channel_name)s - %(levelname)s - FROM %(sender)s TO %(receivers)s WITH %(attachments)s'

    def __init__(self):
        logging.basicConfig(format=self.FORMAT, filename=self.LOG_FILE_PATH, level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

    def logException(self, message):
        self.logger.exception(message)
        return self.logger
    
    def logDebug(self, message):
        self.logger.debug(message)
        return self.logger
    
