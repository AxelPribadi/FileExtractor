# FastAPI to check lancedb data
import lancedb


# Path to LanceDB database
URI = "/Users/axel/Documents/GitHub Repo/FileExtractor/localhouse"

def get_table_data(table_name="test"):
    db = lancedb.connect(URI)

    table = db.open_table(table_name)
    table_data = table.to_pandas().to_dict(orient="records")

    json = {"length":len(table_data), "data": table_data}
    return json


if __name__ == "__main__":
    print(get_table_data())

