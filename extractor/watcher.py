import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from extractor.core.config import settings
from extractor.pipeline.extractor import *

class DownloadsWatcher(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory

    def on_created(self, event):
        if not event.is_directory:
            print(f"new file detected: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"file modified: {event.src_path}")
 
    def get_all_files(self):
        return [
            f for f in os.listdir(self.directory) 
            if os.path.isfile(os.path.join(self.directory, f))
        ]

class Watcher:
    def __init__(self):
        self.directory = settings.DOWNLOADS_FOLDER_PATH
        self.observer = Observer()
        self.event_handler = DownloadsWatcher(self.directory)

    def watch(self):
        self.observer.schedule(
            event_handler=self.event_handler,
            path=settings.DOWNLOADS_FOLDER_PATH,
            recursive=False
        )

        self.observer.start()

        try:
            # last_run_time = time.time()
            ingestor = Ingestor(table_name=settings.LANCE_DB_TABLE_NAME)

            print(f"Current file list: {self.event_handler.get_all_files()}")
            files = self.event_handler.get_all_files()
            ingestor.ingest(files)
            
            while True:
                # run every minute
                # current_time = time.time()
                # if current_time - last_run_time >= 10:
                #     print(f"Current file list: {self.event_handler.get_all_files()}")
                #     files = self.event_handler.get_all_files()
                #     ingestor.ingest(files)
                #     last_run_time = current_time

                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()

        self.observer.join()
