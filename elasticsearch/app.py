from flask import Flask, request, jsonify, flash
from elasticsearch import Elasticsearch
from models import Chunk
from utils import text_splitter,get_extractor
import tempfile
import os
import shutil

app = Flask(__name__)
es_service = Elasticsearch('http://localhost:9200',basic_auth=('elastic','changeme'),verify_certs=False)
app.secret_key = 'tiendoan'
@app.route('/create_index', methods=['POST'])
def create_index():
    data = request.form
    index_name = data['index_name']
    
    if not index_name:
        return jsonify({"error": "Index name is required"}), 400
    if not es_service.indices.exists(index=index_name):
        response = es_service.indices.create(index=index_name, body={
                "mappings": {
                    "properties": {
                        "document_id": {"type": "integer"},
                        "chunk_order": {"type": "integer"},
                        "text": {"type":"text"},
                    }
                }
            })
        return jsonify(response.body), 201  
    return jsonify({"message": "Index already exists"}), 200

@app.route('/delete_index', methods=['DELETE'])
def delete_index():
    data = request.form
    index_name = data["index_name"]
    
    if not index_name:
        return jsonify({"error": "Index name is required"}), 400

    response = es_service.indices.delete(index = index_name)
    return jsonify(response.body)

@app.route('/ingest_data', methods=['POST'])
def ingest_data():
    data = request.form
    document_ids = data['document_ids'].split(' ')
    files = request.files.getlist('files')
    temp_dir = tempfile.mkdtemp()
    
    try:
        for file, document_id in zip(files, document_ids):
            temp_file_path = os.path.join(temp_dir, file.filename)
            file.save(temp_file_path)
            try:
                extractor = get_extractor(file.filename)
                document = extractor.load_data(temp_file_path)
                splits = text_splitter.split_text(document[0].text)
                for idx, split in enumerate(splits):
                    body = {
                        'document_id': int(document_id),
                        'chunk_order': int(idx + 1),
                        "text": split,
                    }
                    es_service.index(index=data['index_name'], body=body, id=f'{document_id}_{idx + 1}')
            except Exception:
                flash(f"Unsupported file type: {file.filename}", 'danger')
                continue
    finally:
        # Xóa thư mục tạm ngay cả khi có lỗi xảy ra
        shutil.rmtree(temp_dir, ignore_errors=True)

    return jsonify({"message": f"{len(files)} document(s) uploaded successfully!"}), 201


@app.route('/delete_data', methods=['DELETE'])
def delete_data():
    data = request.form
    
    response = es_service.delete_by_query(index = data["index_name"], 
                                        query={
                                                "match": {
                                                    "document_id": int(data['document_id'])
                                                }
                                            },                
    )
    return jsonify(response.body)

@app.route('/query', methods=['POST'])
def query():
    data = request.form
    body = {
        "query": {
            "multi_match": {
                "query": data['query'],
                "fields": ["text"]
            }
        }
    }
    
    response = es_service.search(index=data["index_name"],body= body)
    return jsonify(response.body)


if __name__ == '__main__':
    app.run(port=5000,debug=True)
