#!/usr/bin/env python3
"""
api/server.py
- HTTP server using http.server
- CRUD endpoints for /transactions
- Uses data/processed/transactions.json as the backend store
- Basic Authentication required on all endpoints
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import threading
import time
import base64

# Configuration
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))  # api/ -> repo root
DATA_FILE = os.path.join(REPO_ROOT, "data", "processed", "transactions.json")
LOCK = threading.Lock()
PORT = 8000

# Default credentials (override via environment variables)
API_USER = os.getenv("API_USER", "apiuser")
API_PASS = os.getenv("API_PASS", "apipass")

# Ensure processed data dir exists; if not, create and seed minimal file
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
if not os.path.exists(DATA_FILE):
    # create an empty list file so server has something to load
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)


def load_data():
    """Load transactions from JSON and return (list, dict_by_id)."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Ensure integer ids where present
    for item in data:
        if "id" in item:
            try:
                item["id"] = int(item["id"])
            except Exception:
                pass
    data_dict = {item["id"]: item for item in data if "id" in item}
    return data, data_dict


def save_data(data_list):
    """Persist list of transactions to disk atomically."""
    with LOCK:
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)
        os.replace(tmp, DATA_FILE)


def check_basic_auth(headers):
    """Return True if Authorization header matches API_USER/API_PASS."""
    auth = headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        return False
    try:
        b64 = auth.split(" ", 1)[1].strip()
        decoded = base64.b64decode(b64).decode("utf-8")
        user, passwd = decoded.split(":", 1)
        return user == API_USER and passwd == API_PASS
    except Exception:
        return False


class AuthJSONHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _unauthorized(self):
        self.send_response(401)
        # Ask client to present Basic credentials
        self.send_header("WWW-Authenticate", 'Basic realm="MoMoAPI"')
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        body = json.dumps({"error": "unauthorized"}).encode("utf-8")
        self.wfile.write(body)

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # CORS helpful for testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        # Authenticate
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []

        # GET /transactions
        if parts == ["transactions"]:
            data_list, _ = load_data()
            return self._send_json(data_list, status=200)

        # GET /transactions/{id}
        if len(parts) == 2 and parts[0] == "transactions":
            try:
                tid = int(parts[1])
            except ValueError:
                return self._send_json({"error": "invalid id"}, status=400)
            _, data_dict = load_data()
            item = data_dict.get(tid)
            if item is None:
                return self._send_json({"error": "not found"}, status=404)
            return self._send_json(item, status=200)

        return self._send_json({"error": "not found"}, status=404)

    def do_POST(self):
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        if parsed.path != "/transactions":
            return self._send_json({"error": "not found"}, status=404)

        body = self._read_json_body()
        if not body or not isinstance(body, dict):
            return self._send_json({"error": "invalid json body"}, status=400)

        with LOCK:
            data_list, data_dict = load_data()
            max_id = max([item.get("id", 0) for item in data_list], default=0)
            new_id = max_id + 1
            body["id"] = new_id
            if "timestamp" not in body:
                body["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            data_list.append(body)
            save_data(data_list)
        return self._send_json(body, status=201)

    def do_PUT(self):
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
        if len(parts) == 2 and parts[0] == "transactions":
            try:
                tid = int(parts[1])
            except ValueError:
                return self._send_json({"error": "invalid id"}, status=400)
            body = self._read_json_body()
            if not body or not isinstance(body, dict):
                return self._send_json({"error": "invalid json body"}, status=400)
            with LOCK:
                data_list, data_dict = load_data()
                if tid not in data_dict:
                    return self._send_json({"error": "not found"}, status=404)
                body["id"] = tid  # preserve id
                for i, item in enumerate(data_list):
                    if item.get("id") == tid:
                        data_list[i] = body
                        break
                save_data(data_list)
            return self._send_json(body, status=200)
        return self._send_json({"error": "not found"}, status=404)

    def do_DELETE(self):
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
        if len(parts) == 2 and parts[0] == "transactions":
            try:
                tid = int(parts[1])
            except ValueError:
                return self._send_json({"error": "invalid id"}, status=400)
            with LOCK:
                data_list, data_dict = load_data()
                if tid not in data_dict:
                    return self._send_json({"error": "not found"}, status=404)
                data_list = [item for item in data_list if item.get("id") != tid]
                save_data(data_list)
            return self._send_json({"status": "deleted"}, status=200)
        return self._send_json({"error": "not found"}, status=404)


def run(server_class=HTTPServer, handler_class=AuthJSONHandler, port=PORT):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on http://localhost:{port} ...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server")
        httpd.server_close()


if __name__ == "__main__":
    run()

