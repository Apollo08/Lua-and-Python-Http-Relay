from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import requests

# Set mode: "LAN" (for direct Lua interface and forwarding) or "SER" (for relay/secondary)
MODE = "LAN"  # Change to "SER" on the relay/secondary script

# Address of the secondary/relay server (used only in LAN mode)
SER_HOST = "192.168.0.1"
SER_PORT = 8080  # Change as needed

DATA_FILE = "data.txt"

def save_data(value):
    with open(DATA_FILE, "w") as f:
        f.write(str(value))

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def forward_to_ser(value):
    try:
        url = f"http://{SER_HOST}:{SER_PORT}/{value}"
        r = requests.get(url, timeout=0.5)
        return r.status_code == 200
    except Exception as e:
        print(f"Forward error: {e}")
        return False

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/" or parsed.path == "":
            data = load_data()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(data.encode())
        else:
            value = parsed.path.lstrip("/")
            try:
                float(value)  # Validate it's a number
                if MODE == "LAN":
                    # Try to forward, only save as backup if forward fails
                    success = forward_to_ser(value)
                    if not success:
                        save_data(value)
                else:
                    # SER mode: always save
                    save_data(value)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(value.encode())
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid number")

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 5000), SimpleHandler)
    print(f"Server running on http://127.0.0.1:5000 in {MODE} mode")
    server.serve_forever()