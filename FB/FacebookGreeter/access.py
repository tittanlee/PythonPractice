__author__ = 'dgraziotin'
"""
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""
import facebook
import urllib
import warnings
import webbrowser
import dbmanager
import urllib.parse
import settings
import os


class FBOAuth(object):
    """
    Handles the OAuth phases of Facebook and returns an authenticated GrapApi object, to be used for
    using the Facebook API.
    """
    FACEBOOK_GRAPH_URL = settings.FACEBOOK_GRAPH_URL
    CLIENT_ID     = settings.CLIENT_ID
    CLIENT_SECRET = settings.CLIENT_SECRETS
    REDIRECT_URI = settings.REDIRECT_URI

    SECRET_CODE = None
    ACCESS_TOKEN = None

    def __init__(self):
        self.database = dbmanager.DBManager()
        FBOAuth.SECRET_CODE = self.get_secret_code()
        FBOAuth.ACCESS_TOKEN = self.get_access_token()

    def get_secret_code(self):
        # return self.database.get('SECRET_CODE') or None
        return None

    def save_secret_code(self, secret_code):
        self.database.save('SECRET_CODE', secret_code)

    def get_access_token(self):
        return self.database.get('ACCESS_TOKEN') or None

    def save_access_token(self, access_token):
        self.database.save('ACCESS_TOKEN', access_token)

    def authorize(self):
        
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            ie = webbrowser.get(webbrowser.iexplore)
            webbrowser.open('https://www.facebook.com/dialog/oauth?'+urllib.parse.urlencode(
                                {'client_id': FBOAuth.CLIENT_ID,
                                 'redirect_uri':FBOAuth.REDIRECT_URI,
                                 'scope':'read_stream, publish_stream'}))

            # Url = 'https://www.facebook.com/dialog/oauth?' + urllib.parse.urlencode(
            #                     {'client_id': FBOAuth.CLIENT_ID,
            #                      'redirect_uri':FBOAuth.REDIRECT_URI,
            #                      'scope':'read_stream, publish_stream'})

            # print(Url)
            # Sec = urllib.request.request(Url)
            # print(Sec)
        finally:
            os.dup2(savout, 1)
        FBOAuth.SECRET_CODE = input("Secret Code: ")
        self.save_secret_code(FBOAuth.SECRET_CODE)

        return FBOAuth.SECRET_CODE

    def access_token(self):

        if not FBOAuth.SECRET_CODE:
            FBOAuth.SECRET_CODE = self.authorize()

        args = {'redirect_uri': FBOAuth.REDIRECT_URI,
                'client_id' : FBOAuth.CLIENT_ID,
                'client_secret':FBOAuth.CLIENT_SECRET,
                'code':FBOAuth.SECRET_CODE,}
        
        access_token = urllib.request.urlopen(FBOAuth.FACEBOOK_GRAPH_URL + "/oauth/access_token?" + \
                                                urllib.parse.urlencode(args)).read().decode('utf-8')

        print(access_token)

        access_token = urllib.parse.parse_qs(access_token)
        FBOAuth.ACCESS_TOKEN = access_token['access_token'][0]
        self.save_access_token(FBOAuth.ACCESS_TOKEN)
        return FBOAuth.ACCESS_TOKEN

    def get_graph_api(self):

        if not FBOAuth.ACCESS_TOKEN:
            self.access_token()

        return facebook.GraphAPI(FBOAuth.ACCESS_TOKEN)

    def invalidate_login(self):
        self.save_access_token(None)
        self.save_secret_code(None)
        exit(0)

