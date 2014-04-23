import quixote
from quixote.directory import Directory, export, subdir
from quixote.util import StaticFile
import os.path
import sqlite3

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        username = quixote.get_cookie('username')
        if not username:
            username = ''
        vars = dict(username = username)
        return html.render('index.html', vars)

    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.11.0.min.js').read()

    def authenticate(self, username, password):
        db = sqlite3.connect('images.sqlite')

        c = db.cursor()

        # Latest image
        c.execute('SELECT * FROM user where username=(?)', (username,))
        try:
            username, pwd = c.fetchone()
        except:
            return False

        return pwd == password

    def set_cookie(self, username):
        quixote.get_response().set_cookie('username', username)
        return quixote.redirect('./')

    @export(name='logout')
    def logout(self):
        response = quixote.get_response()
        response.set_cookie('username', 'NONE; Expires=Thu, 01-Jan-1970 00:00:01 GMT')
        return quixote.redirect('./')

    @export(name='create_account')
    def create_account(self):
        return html.render('create_account.html')

    @export(name='create_account_receive')
    def create_account_receive(self):
        request = quixote.get_request()
        username = request.form['username']
        password = request.form['password']

        db = sqlite3.connect('images.sqlite')

        c = db.cursor()

        # Latest image
        c.execute('SELECT username FROM user WHERE username=(?)', (username,))

        if(c.fetchone() == None):
            db.execute('INSERT INTO user VALUES (?,?)', (username, password))
            db.commit()


    @export(name='login')
    def login(self):
        return html.render('login.html')

    @export(name='login_receive')
    def login_receive(self):
        request = quixote.get_request()
        username = request.form['username']
        password = request.form['password']

        if(self.authenticate(username, password)):
            return self.set_cookie(username)
        return quixote.redirect("./")

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(the_file.base_filename, data)

        return quixote.redirect('./')

    @export(name='upload2')
    def upload2(self):
        return html.render('upload2.html')

    @export(name='upload2_receive')
    def upload2_receive(self):
        request = quixote.get_request()

        the_file = request.form['file']
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(the_file.get_size())

        image.add_image(the_file.base_filename, data)

        return html.render('upload2_received.html')

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_list')
    def image_list(self):
        return html.render('image_list.html')

    @export(name='image_count')
    def image_count(self):
        return image.get_num_images()

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        img = image.retrieve_image(i)

        filename = img.filename
        if filename.lower() in ('jpg', 'jpeg'):
            response.set_content_type('image/jpeg')
        elif filename.lower() in ('tif',' tiff'):
            response.set_content_type('image/tiff')
        else: # Default to .png for reasons
            response.set_content_type('image/png')
        return img.data

    @export(name='get_comments')
    def get_comments(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        all_comments = []
        for comment in image.get_comments(i):
            all_comments.append("""\
    <comment>
     <text>%s</text>
    </comment>
    """ % (comment))

        xml = """
    <?xml version="1.0"?>
    <comments>
    %s
    </comments>
    """ % ("".join(all_comments))

        return xml

    @export(name='add_comment')
    def add_comment(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        try:
            comment = request.form['comment']
        except:
            return

        image.add_comment(i, comment)

    @export(name='get_score')
    def get_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        return image.get_image_score(i)

    @export(name='increment_score')
    def increment_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        image.increment_image_score(i)

    @export(name='decrement_score')
    def decrement_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        image.decrement_image_score(i)