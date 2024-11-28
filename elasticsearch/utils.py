from langchain.text_splitter import RecursiveCharacterTextSplitter
from read_data.kotaemon.loaders import *
from llama_index.readers.json import JSONReader
from llama_index.readers.file import PandasCSVReader, UnstructuredReader
from elasticsearch import Elasticsearch

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=256,
    chunk_overlap=50
)

def get_extractor(file_name: str):
    map_reader = {
        "docx": DocxReader(),
        "html": UnstructuredReader(),
        "csv": PandasCSVReader(pandas_config=dict(on_bad_lines="skip")),
        "xlsx": PandasExcelReader(),
        "json": JSONReader(),
        "txt": TxtReader()
    }
    return map_reader[file_name.rpartition('.')[-1]]