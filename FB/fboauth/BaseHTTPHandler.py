class HTTPServerHandler(BaseHTTPRequestHandler):

    """
    HTTP Server callbacks to handle Facebook OAuth redirects
    """
    def __init__(self, request, address, server):
        super().__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
