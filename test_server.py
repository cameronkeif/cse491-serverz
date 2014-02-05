import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test basic GET calls.

# Test path = /
def test_handle_connection():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "<p><u>Form Submission via GET</u></p>" + \
                      "<form action='/submit' method='GET'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>" + \
                      "<p><u>Form Submission via POST</u></p>" +\
                      "<form action='/submit' method='POST'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test path = /content
def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Cam is great</h1>' + \
                      'This is some content.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test path = /file
def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>They don\'t think it be like it is, but it do.</h1>' + \
                      'This some file.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test path = /content
def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Wow. Such page. Very HTTP response</h1>' + \
                      'This is some image.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test path = /submit
def test_handle_submit():
    conn = FakeConnection("GET /submit?firstname=T&lastname=Swizzle HTTP/1.0" + \
                          "HTTP/1.1\r\n\r\n")

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Mrs. T Swizzle."

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# test 404
def test_handle_not_found():
    conn = FakeConnection("GET /apple HTTP/1.0\r\n\r\n")

    expected_return = 'HTTP/1.0 404 Not Found\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'Oopsies, this isn\'t the page you want. :('

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test POST connections

# Test / requests
def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "<p><u>Form Submission via GET</u></p>" + \
                      "<form action='/submit' method='GET'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>" + \
                      "<p><u>Form Submission via POST</u></p>" +\
                      "<form action='/submit' method='POST'>\n" + \
                      "<p>first name: <input type='text' name='firstname'></p>\n" + \
                      "<p>last name: <input type='text' name='lastname'></p>\n" + \
                      "<p><input type='submit' value='Submit'>\n\n" + \
                      "</form></p>"

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

# Test /submit requests
def test_handle_submit_post():
    conn = FakeConnection("POST /submit " + \
                          "HTTP/1.1\r\n\r\nfirstname=T&lastname=Swizzle")

    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "Hello Mrs. T Swizzle."

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    

# test 404
def test_handle_not_found_post():
    conn = FakeConnection("POST /apple HTTP/1.0\r\n\r\n")

    expected_return = 'HTTP/1.0 404 Not Found\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      'Oopsies, this isn\'t the page you want. :('

    server.handle_connection(conn)
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
    