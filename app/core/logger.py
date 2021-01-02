from logging import getLogger, StreamHandler, Formatter, INFO


logger = getLogger("FastAPI")
logger.setLevel(INFO)

handler = StreamHandler()

formatter = Formatter("%(asctime)s %(name)s(%(process)d):[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
