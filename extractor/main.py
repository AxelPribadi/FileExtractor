from extractor.core.config import settings
from extractor.pipeline.extractor import *
from extractor.watcher import *

if __name__ == "__main__":

    watcher = Watcher()
    watcher.watch()
