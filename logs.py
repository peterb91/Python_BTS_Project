import logging

logging.basicConfig(filename='myapp.log', format='%(asctime)s %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
