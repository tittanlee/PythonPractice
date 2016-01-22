class TokenHandler:
    """
    Class used to handle Facebook oAuth
    """
    def __init__(self, a_id, a_secret):
        self._id = a_id
        self._secret = a_secret

    def get_access_token(self):
        httpServer = HTTPServer(('localhost', 8080), HTTPServerHandler)

        #Only handle one request, since we should only ever get one request from Facebook.

        httpServer.handle_request()