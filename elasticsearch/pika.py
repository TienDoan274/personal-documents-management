import pika
import json
from elasticsearch import Elasticsearch

# Kết nối đến Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

def callback(ch, method, properties, body):
    # Giải mã message JSON
    document_data = json.loads(body)
    document_id = document_data['document_id']
    document_title = document_data['document_title']
    content = document_data['content']
    
    # Thực hiện ingest dữ liệu vào Elasticsearch
    es.index(index='documents', id=document_id, body={
        'title': document_title,
        'content': content
    })
    print(f"Document {document_id} ingested into Elasticsearch.")

def listen_for_documents():
    # Thiết lập kết nối với RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Đảm bảo rằng queue 'document_events' đã tồn tại
    channel.queue_declare(queue='document_events')

    # Lắng nghe các message trong queue 'document_events'
    channel.basic_consume(queue='document_events', on_message_callback=callback, auto_ack=True)
    
    print("Waiting for document events. To exit press CTRL+C")
    channel.start_consuming()

# Bắt đầu lắng nghe
listen_for_documents()
