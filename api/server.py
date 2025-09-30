#!/usr/bin/env python3
"""
api/server.py
- HTTP server using http.server
- CRUD endpoints for /transactions
- Uses data/processed/sms_records.json as the backend store
- Basic Authentication required on all endpoints
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
import os
import threading
import time
import base64


REPO_ROOT = os.path.dirname(os.path.dirname(__file__))  
DATA_FILE = os.path.join(REPO_ROOT, "data", "processed", "sms_records.json")
LOCK = threading.Lock()
PORT = 8000

# Default credentials 
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
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Ensure all items have integer ids
        for item in data:
            if "id" in item and item["id"] is not None:
                try:
                    item["id"] = int(item["id"])
                except (ValueError, TypeError):
                    # If id conversion fails, skip this item for operations
                    pass
        
        # Create dictionary only for items with valid integer IDs
        data_dict = {}
        for item in data:
            if "id" in item and isinstance(item["id"], int):
                data_dict[item["id"]] = item
        
        return data, data_dict
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading data: {e}")
        return [], {}


def save_data(data_list):
    """Persist list of transactions to disk atomically."""
    try:
        
        # Create a backup first
        backup_file = DATA_FILE + ".backup"
        if os.path.exists(DATA_FILE):
            import shutil
            shutil.copy2(DATA_FILE, backup_file)
        
        # Write directly to the file
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=2, ensure_ascii=False)
        
        # Remove backup if write was successful
        if os.path.exists(backup_file):
            os.remove(backup_file)
            
    except Exception as e:
        print(f"Error saving data: {e}")
        import traceback
        traceback.print_exc()
        
        # Try to restore from backup if write failed
        backup_file = DATA_FILE + ".backup"
        if os.path.exists(backup_file):
            import shutil
            shutil.copy2(backup_file, DATA_FILE)
            os.remove(backup_file)


def check_basic_auth(headers):
    """Return True if Authorization header matches API_USER/API_PASS."""
    auth = headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        return False
    try:
        b64 = auth.split(" ", 1)[1].strip()
        decoded = base64.b64decode(b64).decode("utf-8")
        if ":" not in decoded:
            return False
        user, passwd = decoded.split(":", 1)
        return user == API_USER and passwd == API_PASS
    except Exception as e:
        print(f"Auth error: {e}")
        return False


class AuthJSONHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        """Override to add custom logging"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.command} {self.path} - {format % args}")

    def _unauthorized(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="MoMoAPI"')
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        body = json.dumps({"error": "unauthorized", "message": "Basic authentication required"}).encode("utf-8")
        self.wfile.write(body)

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # CORS headers for testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        content_length = self.headers.get("Content-Length")
        if not content_length:
            return None
        
        try:
            length = int(content_length)
            if length == 0:
                return None
            
            # Read the exact number of bytes specified in Content-Length
            raw = self.rfile.read(length)
            decoded = raw.decode("utf-8")
            parsed = json.loads(decoded)
            return parsed
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as e:
            return None

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_GET(self):
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.strip("/").split("/") if p] if parsed.path.strip("/") else []

        # GET /transactions
        if not parts or parts == ["transactions"]:
            data_list, _ = load_data()
            return self._send_json({
                "data": data_list,
                "count": len(data_list),
                "message": "Transactions retrieved successfully"
            }, status=200)

        # GET /transactions/{id}
        if len(parts) == 2 and parts[0] == "transactions":
            try:
                tid = int(parts[1])
            except ValueError:
                return self._send_json({"error": "invalid_id", "message": "ID must be an integer"}, status=400)
            
            _, data_dict = load_data()
            item = data_dict.get(tid)
            if item is None:
                return self._send_json({"error": "not_found", "message": f"Transaction with ID {tid} not found"}, status=404)
            
            return self._send_json({
                "data": item,
                "message": "Transaction retrieved successfully"
            }, status=200)

        return self._send_json({"error": "not_found", "message": "Endpoint not found"}, status=404)

    def do_POST(self):
        
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        if parsed.path.strip("/") != "transactions":
            return self._send_json({"error": "not_found", "message": "Use POST /transactions to create"}, status=404)

        body = self._read_json_body()
        
        if not body or not isinstance(body, dict):
            return self._send_json({"error": "invalid_body", "message": "Request body must be valid JSON object"}, status=400)

        try:
            with LOCK:
                data_list, data_dict = load_data()
                
                # Generate new ID
                existing_ids = [item.get("id", 0) for item in data_list if isinstance(item.get("id"), int)]
                max_id = max(existing_ids, default=0)
                new_id = max_id + 1
                
                
                # Prepare new item
                body["id"] = new_id
                if "timestamp" not in body:
                    body["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                
              
                # Add to list
                data_list.append(body)
                save_data(data_list)
            
            return self._send_json({
                "data": body,
                "message": f"Transaction created successfully with ID {new_id}"
            }, status=201)
                
        except Exception as e:
            print(f"POST Error: {e}")
            return self._send_json({"error": "server_error", "message": f"Failed to create transaction: {str(e)}"}, status=500)

    def do_PUT(self):
        
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.strip("/").split("/") if p]
        
        if len(parts) != 2 or parts[0] != "transactions":
            return self._send_json({"error": "invalid_path", "message": "Use PUT /transactions/{id} to update"}, status=400)
        
        try:
            tid = int(parts[1])
        except ValueError:
            return self._send_json({"error": "invalid_id", "message": "ID must be an integer"}, status=400)

        body = self._read_json_body()
        if not body or not isinstance(body, dict):
            return self._send_json({"error": "invalid_body", "message": "Request body must be valid JSON object"}, status=400)

        try:
            with LOCK:
                data_list, data_dict = load_data()
                
                if tid not in data_dict:
                    return self._send_json({"error": "not_found", "message": f"Transaction with ID {tid} not found"}, status=404)
                
                # Preserve ID and update item
                body["id"] = tid
                if "updated_at" not in body:
                    body["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
                
                # Find and replace the item
                for i, item in enumerate(data_list):
                    if item.get("id") == tid:
                        data_list[i] = body
                        break
                
                save_data(data_list)
                
                return self._send_json({
                    "data": body,
                    "message": f"Transaction {tid} updated successfully"
                }, status=200)
                
        except Exception as e:
            print(f"PUT Error: {e}")
            return self._send_json({"error": "server_error", "message": f"Failed to update transaction: {str(e)}"}, status=500)

    def do_DELETE(self):
        
        if not check_basic_auth(self.headers):
            return self._unauthorized()

        parsed = urlparse(self.path)
        parts = [p for p in parsed.path.strip("/").split("/") if p]
        
        if len(parts) != 2 or parts[0] != "transactions":
            return self._send_json({"error": "invalid_path", "message": "Use DELETE /transactions/{id} to delete"}, status=400)
        
        try:
            tid = int(parts[1])
        except ValueError:
            return self._send_json({"error": "invalid_id", "message": "ID must be an integer"}, status=400)

        try:
            with LOCK:
                data_list, data_dict = load_data()
                
                if tid not in data_dict:
                    return self._send_json({"error": "not_found", "message": f"Transaction with ID {tid} not found"}, status=404)
                
                # Remove the item
                original_count = len(data_list)
                data_list = [item for item in data_list if item.get("id") != tid]
                
                if len(data_list) == original_count:
                    return self._send_json({"error": "not_found", "message": f"Transaction with ID {tid} not found"}, status=404)
                
                save_data(data_list)
                
                return self._send_json({
                    "message": f"Transaction {tid} deleted successfully",
                    "deleted_id": tid
                }, status=200)
                
        except Exception as e:
            print(f"DELETE Error: {e}")
            return self._send_json({"error": "server_error", "message": f"Failed to delete transaction: {str(e)}"}, status=500)


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
