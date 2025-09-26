#!/usr/bin/env python3
"""
Simple REST API using http.server
- Endpoints:
  GET    /transactions
  GET    /transactions/{id}
  POST   /transactions
  PUT    /transactions/{id}
  DELETE /transactions/{id}

Data persistence: data/sms_records.json (created if missing)
This file is self-contained and intended for AURORE's assignment deliverable.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import threading
import time

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
DATA_FILE = os.path.join(DATA_DIR, 'sms_records.json')
LOCK = threading.Lock()
PORT = 8000

# Helper: ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Sample seed data (used if DATA_FILE does not exist)
SAMPLE = [
    {"id": 1, "sender": "+250780000001", "receiver": "+250780000002", "amount": 1200.0, "timestamp": "2025-09-25T10:00:00", "message": "Payment for groceries"},
    {"id": 2, "sender": "+250780000003", "receiver": "+250780000001", "amount": 5000.0, "timestamp": "2025-09-25T12:30:00", "message": "Rent contribution"}
]


def load_data():
    """Load list of transactions from disk. Returns (list, dict).
    Dict maps id -> record for fast lookup.
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(SAMPLE, f, indent=2)
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # ensure ids are ints
    for item in data:
        item['id'] = int(item['id'])
    data_dict = {item['id']: item for item in data}
    return data, data_dict


def save_data(data_list):
    """Persist list of transactions to disk (atomic-ish)."""
    with LOCK:
        tmp = DATA_FILE + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, indent=2)
        os.replace(tmp, DATA_FILE)


class SimpleJSONHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        # CORS (helpful for quick testing with browsers/postman)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode('utf-8'))
        except Exception:
            return None

    def do_OPTIONS(self):
        # For CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip('/').split('/') if parsed.path.strip('/') else []

        # GET /transactions
        if parts == ['transactions']:
            data_list, _ = load_data()
            return self._send_json(data_list, status=200)

        # GET /transactions/{id}
        if len(parts) == 2 and parts[0] == 'transactions':
            try:
                tid = int(parts[1])
            except ValueError:
                return self._send_json({'error': 'invalid id'}, status=400)
            data_list, data_dict = load_data()
            item = data_dict.get(tid)
            if item is None:
                return self._send_json({'error': 'not found'}, status=404)
            return self._send_json(item, status=200)

        return self._send_json({'error': 'not found'}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != '/transactions':
            return self._send_json({'error': 'not found'}, status=404)
        body = self._read_json_body()
        if not body or not isinstance(body, dict):
            return self._send_json({'error': 'invalid json body'}, status=400)

        with LOCK:
            data_list, data_dict = load_data()
            # assign new id
            max_id = max([item['id'] for item in data_list], default=0)
            new_id = max_id + 1
            body['id'] = new_id
            # add timestamp if missing
            if 'timestamp' not in body:
                body['timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S')
            data_list.append(body)
            data_dict[new_id] = body
            save_data(data_list)
        self._send_json(body, status=201)

    def do_PUT(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip('/').split('/') if parsed.path.strip('/') else []
        if len(parts) == 2 and parts[0] == 'transactions':
            try:
                tid = int(parts[1])
            except ValueError:
                return self._send_json({'error': 'invalid id'}, status=400)
            body = self._read_json_body()
            if not body or not isinstance(body, dict):
                return self._send_json({'error': 'invalid json body'}, status=400)
            with LOCK:
                data_list, data_dict = load_data()
                if tid not in data_dict:
                    return self._send_json({'error': 'not found'}, status=404)
                # Update record in-place (preserve id)
                body['id'] = tid
                for i, item in enumerate(data_list):
                    if item['id'] == tid:
                        data_list[i] = body
                        break
                data_dict[tid] = body
                save_data(data_list)
            return self._send_json(body, status=200)
        return self._send_json({'error': 'not found'}, status=404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        parts = parsed.path.strip('/').split('/') if parsed.path.strip('/') else []
        if len(parts) == 2 and parts[0] == 'transactions':
            try:
                tid = int(parts[1])
            except ValueError:
                return self._send_json({'error': 'invalid id'}, status=400)
            with LOCK:
                data_list, data_dict = load_data()
                if tid not in data_dict:
                    return self._send_json({'error': 'not found'}, status=404)
                data_list = [item for item in data_list if item['id'] != tid]
                save_data(data_list)
            # 204 No Content (but we return JSON for easier debugging)
            return self._send_json({'status': 'deleted'}, status=200)
        return self._send_json({'error': 'not found'}, status=404)


def run(server_class=HTTPServer, handler_class=SimpleJSONHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on http://localhost:{port} ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down server')
        httpd.server_close()


if __name__ == '__main__':
    run()

