import os
from django.utils import simplejson
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Event(db.Model):
    when = db.DateProperty()
    what = db.StringProperty()
    where = db.StringProperty()

class Person(Event):
    zoom_level = db.IntegerProperty()
    southwest = db.StringProperty()
    northeast = db.StringProperty()

class Activity(Event):
    author = db.StringProperty()

class Explorer(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        greeting = ""
        location, zoom = "13.061252,80.299244", 13
        if not user:
            greeting = "Sign in, or register"
        else:
            person = Person.get_or_insert(user.user_id())
            if person.where is not None:
                location = person.where
            if person.zoom_level is not None:
                zoom = person.zoom_level
        values = {
            'greeting' : greeting,
            'url' : users.create_login_url("/"),
            'user' : user,
            'location' : location,
            'zoom' : zoom,
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, values))

class Saver(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        json = simplejson.loads(self.request.body)
        if user:
            person = Person(key_name=user.user_id(), where=json["center"], zoom_level=json["zoom"], southwest=json["southwest"], northeast=json["northeast"])
            person.put()
        self.response.out.write(self.request.body)

class Adder(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        json = simplejson.loads(self.request.body)
        if user:
            activity = Activity(where=json["location"], author=user.user_id(), what=json["description"])
            activity.put()
        self.response.out.write(self.request.body)

application = webapp.WSGIApplication([('/', Explorer),('/save', Saver),('/add', Adder)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
