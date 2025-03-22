from extractor.core.config import settings
from extractor.pipeline.extractor import *

from extractor.watcher import *

# call watcher to watch downloads folder
# call extractor to process the file

if __name__ == "__main__":

    watcher = Watcher()
    watcher.watch()
    

    # files = []

    # # ingestor.ingest(files)

    # ingestor = Ingestor(
    #     table_name=settings.LANCE_DB_TABLE_NAME
    # )


    # vdb = ingestor.build_vector_db()

    # knowledge_base1 = PDFKnowledgeBase(
    #     path="downloads/documentContext/Processed/documentContext_upsert_DF-GANeXt-paper_20250322165051.pdf",
    #     vector_db=vdb,
    #     reader=PDFImageReader(chunk=True),
    #     chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
    # )

    # knowledge_base2 = PDFKnowledgeBase(
    #     path="downloads/documentContext/Processed/documentContext_reset_deepfake-adapter_20250322165039.pdf",
    #     vector_db=vdb,
    #     reader=PDFImageReader(chunk=True),
    #     chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
    # )

    # print(knowledge_base1)

    # print(knowledge_base2)
 
    
    # knowledge_bases = CombinedKnowledgeBase(
    #     vector_db=vdb,
    #     sources=[
    #         knowledge_base1,
    #         knowledge_base2
    #     ]
    # )

    # print(knowledge_bases)

    # knowledge_bases.load(recreate=True)

