import logging

# ANSI color codes
COLOR_RESET = "\033[0m"
COLORS = {
    'DEBUG': "\033[92m",    # Green
    'INFO': "\033[94m",     # Blue
    'WARNING': "\033[93m",  # Yellow
    'ERROR': "\033[91m",    # Red
    'CRITICAL': "\033[1;91m" # Red and big
}
class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, "")
        message = super().format(record)
        return f"{color}{message}{COLOR_RESET}"



def setup_logger(name: str) -> logging.Logger:
    """Returns a logger instance with console + file handler"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # or INFO in production

    # allows just one instance of the logger --> initialise it only once
    # if the logger already has handlers, we don't want to add more!
    if not logger.handlers:

        # Console Handler with colors
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        color_formatter = ColorFormatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
        console.setFormatter(color_formatter)
        logger.addHandler(console)

        # File Handler without colors
        file = logging.FileHandler('logs/beautyshop.log')
        file.setLevel(logging.INFO)
        file_formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(name)s: %(message)s')
        file.setFormatter(file_formatter)
        logger.addHandler(file)

    return logger