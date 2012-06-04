from google.appengine.ext import db

class User(db.Expando):
    pass

class Page(db.Expando):
    # created_by
    # created_date
    # content
    created = db.DateTimeProperty(auto_now_add=True)
    pass
