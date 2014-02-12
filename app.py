# from http://docs.python.org/2/library/wsgiref.html

import jinja2
from wsgiref.util import setup_testing_defaults

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)

    # By default, set up the 404 page response. If it's
    # a valid page, we change this. If some weird stuff
    # happens, it'll default to 404.
    status = '404 Not Found'
    response_content = not_found('', env)
    headers = [('Content-type', 'text/html')]
    
    http_method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    if http_method == 'POST':
        form = cgi.FieldStorage(headers = headers_dict, fp = StringIO(content),
                                environ = environ)
        if path == '/':
            status = '200 OK'
            response_content = handle_index('', env)
            
        elif path == '/submit':
        	pass
                # POST has parameters at the end of content body
                #handle_submit_post(conn, form, env)
    elif http_method == 'GET':
        if path == '/':
            status = '200 OK'
            response_content = handle_index('', env)
        elif path == '/content':
            status = '200 OK'
            response_content = handle_content('', env)
        elif path == '/file':
            status = '200 OK'
            response_content = handle_file('', env)
        elif path == '/image':
            status = '200 OK'
            response_content = handle_image('', env)
        elif path == '/submit':
            pass
                #handle_submit_get(conn, parsed_url[4], env)
                
    start_response(status, headers)
    return response_content

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

def not_found(params, env):
    return str(env.get_template("not_found.html").render())