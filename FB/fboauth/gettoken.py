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
        if 'code' in self.path:
            self.auth_code = self.path.split('=')[1]
            #Display to the user that they no longer need the browser window
            self.wfile.write(bytes('<html><h1>You may now close this window.'
                              + '</h1></html>', 'utf-8'))
            self.server.access_token = get_access_token_from_url(
                    GRAPH_API_AUTH_URI + self.auth_code)