import logging

# Configure the logging settings
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level of messages to log
    format="%(asctime)s [%(levelname)s]: %(message)s",  # Define the log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Define the date/time format
)

def get_logger(name):
    return logging.getLogger(name)
