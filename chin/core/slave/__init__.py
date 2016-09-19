import logging

logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s @ %(filename)s %(lineno)d]\t%(asctime)s\t%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger("chin")
