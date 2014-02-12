# from http://docs.python.org/2/library/wsgiref.html

import jinja2
from wsgiref.util import setup_testing_defaults

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    status = '200 OK'
    headers = [('Content-type', 'text/html')]

    start_response(status, headers)

    ret = ["%s: %s\n" % (key, value)
           for key, value in environ.iteritems()]
    ret.insert(0, "This is your environ.  Hello, world!\n\n")

    http_method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    print path
    if http_method == 'POST':
        # Printing the request
        form = cgi.FieldStorage(headers = headers_dict, fp = StringIO(content), environ = environ)

        if path == '/':
            return handle_index(conn, '', env)
            
        elif path == '/submit':
        	pass
                # POST has parameters at the end of content body
                #handle_submit_post(conn, form, env)
        else:
        	pass
                #not_found(conn, '', env)
    elif http_method == 'GET':
        #print request
        print 'GET' # debug
        if path == '/':
            return handle_index('', env)
        elif path == '/content':
            pass
                #handle_content(conn, '', env)
        elif path == '/file':
            pass
                #handle_file(conn, '', env)
        elif path == '/image':
            pass
                #handle_image(conn, '', env)
        elif path == '/submit':
            pass
                #handle_submit_get(conn, parsed_url[4], env)
        else:
            pass
                #not_found(conn, '', env)
    else:
    	pass
    	#not_found(conn, '', env)
    return ret

def make_app():
    return simple_app

def handle_index(params, env):
    return str('HTTP/1.0 200 OK\r\n' + \
	       'Content-type: text/html\r\n\r\n' + \
               env.get_template("index_result.html").render())
    
    