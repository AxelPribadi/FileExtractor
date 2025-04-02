from app.core.config import settings
from app.pipeline.extractor import *
from app.watcher import *

if __name__ == "__main__":

    watcher = Watcher()
    watcher.watch()
