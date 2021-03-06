import webapp2
from handlers.users import Signup, Login, Logout, Welcome
from handlers.wiki import WikiPage, EditPage

DEBUG = True

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
    ('/signup', Signup),
    ('/welcome', Welcome),
    ('/login', Login),
    ('/logout', Logout),
    ('/_edit' + PAGE_RE, EditPage),
    (PAGE_RE, WikiPage), ],
    debug=DEBUG)

