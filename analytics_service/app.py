# analytics_service/app.py
from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)
es = Elasticsearch([os.environ.get('ELASTICSEARCH_URL', 'http://localhost:9200')])

@app.route('/log_event', methods=['POST'])
def log_event():
    event_data = request.json
    
    if not event_data:
        return jsonify({"status": "error", "message": "Missing event data"}), 400

    # Vulnerability: No input sanitization
    es.index(index="events", body=event_data)
    
    return jsonify({"status": "success", "message": "Event logged"})

@app.route('/get_stats', methods=['GET'])
def get_stats():
    # Vulnerability: Potential for Denial of Service
    # This query could be resource-intensive if the dataset is large
    result = es.search(index="events", body={
        "size": 0,
        "aggs": {
            "total_views": {"sum": {"field": "views"}},
            "avg_likes": {"avg": {"field": "likes"}},
            "user_count": {"cardinality": {"field": "user_id"}}
        }
    })
    
    stats = result['aggregations']
    return jsonify({"status": "success", "stats": stats})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)