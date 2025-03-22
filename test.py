if __name__ == "__main__":

    from extractor.pipeline.extractor import *
    from extractor.watcher import *
    # for i in range(10, 0, -1):
    #     print(i)


    # files = [
    #     "imageGenerator_reset_chromakopia_20250316143555.png",
    #     "imageGenerator_upsert_chromakopia-2_20250316143535.png",
    #     "imageGenerator_upsert_chromakopia-4_20250316143513.png",
    #     "imageGenerator_upsert_chromakopia-4_20250316143535.png"
    # ]

    # sorted_files = optimizer(sort_files(files))

    # for i in sorted_files:
    #     print(i)
    
    # ingestor = Ingestor(table_name=settings.LANCE_DB_TABLE_NAME)
    # files = Watcher().event_handler.get_all_files()
    # print(f"SORTED: {sort_files(files)}")
    # ingestor.ingest(files)
