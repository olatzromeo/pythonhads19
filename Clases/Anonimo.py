import webapp2
from google.appengine.ext import ndb
from Preguntas import Pregunta

class Anonimo(ndb.Model):
    nick = ndb.StringProperty()
    aciertos = ndb.IntegerProperty()
    fallos = ndb.IntegerProperty()
    creado = ndb.DateTimeProperty(auto_now_add = True)