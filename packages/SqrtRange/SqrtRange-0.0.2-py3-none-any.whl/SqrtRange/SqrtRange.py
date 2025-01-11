import math
import logging
import configparser

config = configparser.ConfigParser()

def Calculate(startingnumber, endingnumber, logFile, doClearLogFile):
    if doClearLogFile:
        with open(logFile, 'w'):
            pass #We write blank to clear the log file
    else:
        pass
    # Initialize logging
    logging.basicConfig(level=logging.DEBUG, filename=logFile, filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    
    for i in range(startingnumber, endingnumber):
        try:
            log_message = "Current number: " + str(i) + " sqrt: "+ str(math.sqrt(i))
            print(log_message)
            logging.info(log_message)
        except ValueError:
            log_message = "Invalid number for sqrt function: " + str(i)
            print(log_message)
            logging.info(log_message)
