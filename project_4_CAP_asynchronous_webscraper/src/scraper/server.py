import http.server
import socketserver
import os

PORT = 8080
Directory = "../static_pages"

class Handler(http.server.SimpleHTTPRequestHandler):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, directory=Directory, **kwargs)
		
with socketserver.TCPServer(("", PORT), Handler) as httpd:
	print(f"serving at port {PORT}")
	httpd.serve_forever()
