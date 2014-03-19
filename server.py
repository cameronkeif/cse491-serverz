#!/usr/bin/env python
import random
import socket
import time
import urlparse
import os
import sys
import argparse
import imageapp
import quixote
import quixote.demo.altdemo
import app

from StringIO import StringIO

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description='Server for several WSGI apps')
    parser.add_argument('-p', metavar='-p', type=int, nargs='?', default=8000,
                   help='an integer for the port number')

    parser.add_argument('-A', metavar='-A', type=str, nargs=1,
                   help='the app to run (image, altdemo, or myapp)')

    args = parser.parse_args()
    appname = args.A[0]

    if appname != "myapp" and appname != "image" and appname != "altdemo":
      raise Exception("Invalid application name. Please enter 'myapp', 'image', or 'altdemo'")
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = args.p

    if port < 8000 or port > 9999:
      print "Invalid port number. Setting to default port number 8000."
      port = 8000


    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port, '\n'
        handle_connection(c, host, port, appname)

def handle_connection(conn, host, port, appname):
  environ = dict(os.environ.items())
  environ['wsgi.errors']       = sys.stderr
  environ['wsgi.version']      = (1, 0)
  environ['wsgi.multithread']  = False
  environ['wsgi.multiprocess'] = True
  environ['wsgi.run_once']     = True
  environ['wsgi.url_scheme']   = 'http'
  environ['SERVER_NAME']       = host
  environ['SERVER_PORT']       = str(port)
  environ['SCRIPT_NAME']       = ''

  request = conn.recv(1)
  
  # This will get all the headers
  while request[-4:] != '\r\n\r\n':
    request += conn.recv(1)

  first_line_of_request_split = request.split('\r\n')[0].split(' ')

  # Path is the second element in the first line of the request
  # separated by whitespace. (Between GET and HTTP/1.1). GET/POST is first.
  http_method = first_line_of_request_split[0]
  environ['REQUEST_METHOD'] = first_line_of_request_split[0]

  try:
    parsed_url = urlparse.urlparse(first_line_of_request_split[1])
    environ['PATH_INFO'] = parsed_url[2]
  except:
    pass

  def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

  if environ['REQUEST_METHOD'] == 'POST':
    environ = parse_post_request(conn, request, environ)
    environ['QUERY_STRING'] = ''
  elif environ['REQUEST_METHOD'] == 'GET':
    environ['QUERY_STRING'] = parsed_url.query
    environ['wsgi.input'] = StringIO('')
  
  # Create the appropriate wsgi app based on the command-line parameter
  if appname == "image":
      try:
          # Sometimes this gets called multiple times. Blergh.
          p = imageapp.create_publisher()
      except RuntimeError:
          pass
    
      imageapp.setup()
      wsgi_app = quixote.get_wsgi_app()
  elif appname == "myapp":
      wsgi_app = app.make_app()
  elif appname == "altdemo":
      try:
        p = quixote.demo.altdemo.create_publisher()
      except RuntimeError:
        pass

    wsgi_app = quixote.get_wsgi_app()

  result = wsgi_app(environ, start_response)
  try:
    for response in result:
      conn.send(response)
  finally:
    if hasattr(result, 'close'):
      result.close()
  conn.close()

def parse_post_request(conn, request, environ):
  request_split = request.split('\r\n')

  # Headers are separated from the content by '\r\n'
  # which, after the split, is just ''.

  # First line isn't a header, but everything else
  # up to the empty line is. The names are separated
  # from the values by ': '
  for i in range(1,len(request_split) - 2):
      header = request_split[i].split(': ', 1)

      if header[0].upper() == 'COOKIE':
        environ['HTTP_COOKIE'] = header[1]
      else:
        environ[header[0].upper()] = header[1]
  
  if 'HTTP_COOKIE' not in environ.keys():
    environ['HTTP_COOKIE'] = ''
    
  content_length = int(environ['CONTENT-LENGTH'])
  
  content = ''
  for i in range(0,content_length):
      content += conn.recv(1)

  environ['wsgi.input'] = StringIO(content)
  return environ

if __name__ == '__main__':
   main()
