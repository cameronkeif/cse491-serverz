# image handling API
import sqlite3
import sys

class Image:
    filename = ''
    data = ''
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

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
def retrieve_image(i):
    # connect to database
    db = sqlite3.connect('images.sqlite')
    
    # configure to retrieve bytes, not text
    db.text_factory = bytes

    # get a query handle (or "cursor")
    c = db.cursor()

    # select all of the images
    if i >= 0:
        c.execute('SELECT i, filename, image FROM image_store where i=(?)', (i,))
    else:
        c.execute('SELECT i, filename, image FROM image_store ORDER BY i DESC LIMIT 1')

    # grab the first result (this will fail if no results!)
    try:
        i, filename, image = c.fetchone()

        retrieved_image = Image(filename, image)

        return Image(filename, image)
    except:
        pass

def add_comment(i, comment):
    db = sqlite3.connect('images.sqlite')
   
    if i == -1:
        c = db.cursor()

        # Latest image
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return

    db.execute('INSERT INTO image_comments (imageId, comment) VALUES (?,?)', (i, comment))
    db.commit()

def get_comments(i):
    comments = []
    db = sqlite3.connect('images.sqlite')

    # Get all the comments for this image
    c = db.cursor()
    if i == -1:
        # Latest image
        c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return

    c.execute('SELECT i, comment FROM image_comments WHERE imageId=(?) ORDER BY i DESC', (i,))
    for row in c:
        comments.append(row[1])

    return comments

def get_num_images():
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT i FROM image_store ORDER BY i DESC LIMIT 1')
    try:
        return int(c.fetchone()[0])
    except:
        return 0