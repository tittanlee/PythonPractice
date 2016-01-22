        ACCESS_URI = ('https://www.facebook.com/dialog/' 
            + 'oauth?client_id=' +self._id + '&redirect_uri='
            + REDIRECT_URL + "&scope=xxxxx")

        open_new(ACCESS_URI)