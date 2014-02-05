# @comment   I Reviewed this, it works it both Firefox and Chrome. Good work!

#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
from StringIO import StringIO

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port, '\n'
        handle_connection(c)

def handle_connection(conn):
  request = conn.recv(1000)
  print request

  first_line_of_request_split = request.split('\r\n')[0].split(' ')

  # Path is the second element in the first line of the request
  # separated by whitespace. (Between GET and HTTP/1.1). GET/POST is first.
  http_method = first_line_of_request_split[0]
	
  try:
    parsed_url = urlparse.urlparse(first_line_of_request_split[1])
    path = parsed_url[2]
  except:
    path = "/404"

  if http_method == 'POST':
    headers_dict, content = parse_post_request(request)
    environ = {}
    environ['REQUEST_METHOD'] = 'POST'

    form = cgi.FieldStorage(headers = headers_dict, fp = content, environ = environ)

    if path == '/':
      handle_index(conn, '')
    elif path == '/submit':
        # POST has the submitted params at the end of the content body
        handle_submit_post(conn,form)
    else:
        notfound(conn,'')
  else:
      # Most of these are taking in empty strings. The assignment
      # said to try to keep all the params the same for the future, so I did.
      if path == '/':
          handle_index(conn,'')
      elif path == '/content':
          handle_content(conn,'')
      elif path == '/file':
          handle_filepath(conn,'')
      elif path == '/image':
          handle_image(conn,'')
      elif path == '/submit':
          # GET has the params in the URL.
          handle_submit_get(conn,parsed_url[4])
      else:
          notfound(conn,'')
  conn.close()

def handle_index(conn, params):
  ''' Handle a connection given path / '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            "<p><u>Form Submission via GET</u></p>"
            "<form action='/submit' method='GET'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>" + \
            "<p><u>Form Submission via POST (multipart/form-data)</u></p>"
            "<form action='/submit' method='POST' enctype='multipart/form-data'>\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>" + \
            "<p><u>Form Submission via POST</u></p>"
            "<form action='/submit' method='POST'\n" + \
            "<p>first name: <input type='text' name='firstname'></p>\n" + \
            "<p>last name: <input type='text' name='lastname'></p>\n" + \
            "<p><input type='submit' value='Submit'>\n\n" + \
            "</form></p>")

def handle_submit_post(conn, form):
    ''' Handle a connection given path /submit '''
    # submit needs to know about the query field, so more
    # work needs to be done here.

    # we want the first element of the returned list

    try:
      firstname = form['firstname'].value
    except KeyError:
      firstname = ''
    try:
      lastname = form['lastname'].value
    except KeyError:
      lastname = ''

    # Screw the patriarchy! Why's it gotta be "Mr."?! - @CTB, hah!
    conn.send('HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n' + \
              "Hello Mrs. %s %s." % (firstname, lastname))

def handle_submit_get(conn, params):
    ''' Handle a connection given path /submit '''
    # submit needs to know about the query field, so more
    # work needs to be done here.

    # we want the first element of the returned list
    params = urlparse.parse_qs(params)

    try:
      firstname = params['firstname'][0]
    except KeyError:
      firstname = ''
    try:
      lastname = params['lastname'][0]
    except KeyError:
      lastname = ''

    # Screw the patriarchy! Why's it gotta be "Mr."?! - @CTB, hah!
    conn.send('HTTP/1.0 200 OK\r\n' + \
              'Content-type: text/html\r\n' + \
              '\r\n' + \
              "Hello Mrs. %s %s." % (firstname, lastname))

def handle_content(conn, params):
  ''' Handle a connection given path /content '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>Cam is great</h1>' + \
            'This is some content.')

def handle_filepath(conn, params):
  ''' Handle a connection given path /file '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>They don\'t think it be like it is, but it do.</h1>' + \
            'This some file.')

def handle_image(conn, params):
  ''' Handle a connection given path /image '''
  conn.send('HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            '<h1>Wow. Such page. Very HTTP response</h1>' + \
            'This is some image.')

def notfound(conn, params):
  conn.send('HTTP/1.0 404 Not Found\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n' + \
            'Oopsies, this isn\'t the page you want. :(')

def parse_post_request(request):
  ''' Takes in a request (as a string), parses it, and
      returns a dictionary of header name => header value 
      returns a StringIO object built from the content of the request
      Sidenote: God I love that you can do this in Python. Python is great.'''
  header_dict = dict()

  request = request.split('\r\n')

  # Headers are separated from the content by '\r\n'
  # which, after the split, is just ''.
  separation_line_index = request.index('')

  # First line isn't a header, but everything else
  # up to the empty line is. The names are separated
  # from the values by ': '
  for i in range(1,separation_line_index):
    header = request[i].split(': ', 1)
    header_dict[header[0].lower()] = header[1]

  # Originally separated by '\r\n' so make sure we put it back in, in case
  # there are multiple lines!
  
  content = StringIO('\r\n'.join(request[separation_line_index + 1:]))

  return header_dict, content

if __name__ == '__main__':
   main()
