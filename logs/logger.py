import logging
frmt = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=frmt, filename='logs/app.log')
logger = logging.getLogger(__name__)
