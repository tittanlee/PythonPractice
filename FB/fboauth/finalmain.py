class TokenHandler:
    """
    Class used to handle Facebook oAuth
    """
    def __init__(self, a_id, a_secret):
        self._id = a_id
        self._secret = a_secret

    def get_access_token(self):
        """
         Fetches the access key using an HTTP server to handle oAuth
         requests
            Args:
                appId:      The Facebook assigned App ID
                appSecret:  The Facebook assigned App Secret
        """

        ACCESS_URI = ('https://www.facebook.com/dialog/' 
            + 'oauth?client_id=' +self._id + '&redirect_uri='
            + REDIRECT_URL + "&scope=ads_management")

        open_new(ACCESS_URI)
        httpServer = HTTPServer(
                ('localhost', PORT),
                lambda request, address, server: HTTPServerHandler(
                    request, address, server, self._id, self._secret))
        #This function will block until it receives a request
        httpServer.handle_request()
        #Return the access token
        return httpServer.access_token 