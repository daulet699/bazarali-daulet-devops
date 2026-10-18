"""Small dependency-free HTTP application for the DevOps lab."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from app.info import get_student_info, format_student_info


class StudentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/health":
            self.respond(200, "application/json; charset=utf-8", json.dumps({"status": "ok"}))
        elif path == "/json":
            self.respond(200, "application/json; charset=utf-8", json.dumps(get_student_info()))
        elif path == "/":
            self.respond(200, "text/plain; charset=utf-8", format_student_info(get_student_info()))
        else:
            self.respond(404, "text/plain; charset=utf-8", "404 Not Found\n")

    def respond(self, status, mime, body):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def main():
    port = int(os.getenv("PORT", "8080"))
    print(format_student_info(get_student_info()), flush=True)
    server = ThreadingHTTPServer(("0.0.0.0", port), StudentHandler)
    print(f"HTTP server running on port {port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
