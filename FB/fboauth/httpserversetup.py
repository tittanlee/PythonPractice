class HTTPServerHandler(BaseHTTPRequestHandler):

    """
    HTTP Server callbacks to handle Facebook OAuth redirects
    """
    def __init__(self, request, address, server, a_id, a_secret):
        self.app_id = a_id
        self.app_secret = a_secret
        super().__init__(request, address, server)

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

class TokenHandler:
    """
    Class used to handle Facebook oAuth
    """
    def __init__(self, a_id, a_secret):
        self._id = a_id
        self._secret = a_secret

    def get_access_token(self):
        httpServer = HTTPServer(('localhost', PORT),
                lambda request, address, server: HTTPServerHandler(request, address, server, self._id, self._secret))
        httpServer.handle_request()