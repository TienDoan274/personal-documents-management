class Chunk:
    def __init__(self,document_id:int,chunk_order:int,text:str):
        self.document_id = document_id
        self.chunk_order = chunk_order
        self.text = text
    def get_id(self):
        return '{self.document_id}_{self_chunk_order}'