class HTTPServerHandler(BaseHTTPRequestHandler):

    """
    HTTP Server callbacks to handle Facebook OAuth redirects
    """
    def __init__(self, request, address, server, a_id, a_secret):
        self.app_id = a_id
        self.app_secret = a_secret
        super().__init__(request, address, server)

    def do_GET(self):
        GRAPH_API_AUTH_URI = ('https://graph.facebook.com/v2.2/oauth/' 
            + 'access_token?client_id=' + self.app_id + '&redirect_uri=' 
            + REDIRECT_URL + '&client_secret=' + self.app_secret + '&code=')

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()