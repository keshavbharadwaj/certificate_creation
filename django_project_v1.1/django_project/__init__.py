import logging
import logging.handlers                                                                             

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')                              #LOGGING ERROR FORMAT TIME, SEVERITY LEVEL, MESSAGE

file_handler = logging.FileHandler('Login.log')                                                     #FILE TO LOG ERRORS
file_handler.setLevel(logging.DEBUG)                                                                #ABOVE DEBUG LEVEL LOG EVERY ERROR
file_handler.setFormatter(formatter)                                                                #LOG ERRORS AS SPECIFIED BY FORMAT

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
