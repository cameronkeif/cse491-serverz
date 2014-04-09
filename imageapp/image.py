# image handling API
import sqlite3
import sys

class Image:
    filename = ''
    data = ''
    comments = []
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments

images = {}

def add_image(filename, data):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0

    image = Image(filename, data)
    images[image_num] = image

    # insert to database
    insert_image(filename, data)

    return image_num

def get_image(num):
    return retrieve_image(num)

def get_latest_image():
    return retrieve_image(-1)

def insert_image(filename, data):
    # connect to the already existing database
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes

    # grab whatever it is you want to put in the database

    # insert!
    db.execute('INSERT INTO image_store (filename, image) VALUES (?,?)', (filename, data))
    db.commit()

# retrieve an image from the database.
def retrieve_image(i = -1):
    # connect to database
    db = sqlite3.connect('images.sqlite')
    
    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    if i >= 0:
        c.execute('SELECT i, filename, image FROM image_store where i=(?)', i)
    else:
        c.execute('SELECT i, filename, image FROM image_store ORDER BY i DESC LIMIT 1')

    # grab the first result (this will fail if no results!)
    try:
        i, filename, image = c.fetchone()
        print image
        print filename

        return Image(filename, image)
    except:
        pass