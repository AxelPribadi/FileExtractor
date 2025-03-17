
import lancedb
import pyarrow as pa

uri = "/Users/axel/Documents/GitHub Repo/FileExtractor/localhouse"
db = lancedb.connect(uri)

print(db.table_names())

table = db.open_table("a")

print(table.to_pandas())


