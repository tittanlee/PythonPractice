def get_access_token_from_url(url):
    """
    Parse the access token from Facebook's response
    Args:
        uri: the facebook graph api oauth URI containing valid client_id,
             redirect_uri, client_secret, and auth_code arguements
    Returns:
        a string containing the access key 
    """
    token = str(urlopen(url).read(), 'utf-8')
    return token.split('=')[1].split('&')[0]