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

    http_method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']
    print path
    if http_method == 'POST':
        # Printing the request
        form = cgi.FieldStorage(headers = headers_dict, fp = StringIO(content), environ = environ)

        if path == '/':
            return handle_index('', env)
            
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
            return handle_content('', env)
        elif path == '/file':
            return handle_file('', env)
        elif path == '/image':
            return handle_image('', env)
        elif path == '/submit':
            pass
                #handle_submit_get(conn, parsed_url[4], env)
        else:
            pass
                #not_found(conn, '', env)
    else:
    	pass
    	#not_found(conn, '', env)
    return ''

def make_app():
    return simple_app

def handle_index(params, env):
    return str(env.get_template("index_result.html").render())
    
def handle_content(params, env):
    return str(env.get_template("content_result.html").render())

def handle_file(params, env):
    return str(env.get_template("file_result.html").render())

def handle_image(params, env):
    return str(env.get_template("image_result.html").render())