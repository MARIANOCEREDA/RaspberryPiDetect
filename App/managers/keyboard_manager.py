import subprocess
from config.logger_config import get_logger

logger = get_logger("KeyboardManager")

kb_process_name = "onboard"

def run_keyboard():
    
    try:
        subprocess.Popen([kb_process_name])

    except Exception as e:
        logger.error(f"Error when trying to run {kb_process_name}:{e}")


def stop_keyboard():

    try:
        subprocess.Popen(["pkill", kb_process_name])

    except Exception as e:
        logger.error(f"Error when trying to stop {kb_process_name}:{e}")