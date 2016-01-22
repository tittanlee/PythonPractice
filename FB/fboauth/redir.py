from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen, HTTPError
from webbrowser import open_new

REDIRECT_URL = 'http://localhost:8080/'