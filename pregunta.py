import webapp2
import os
import jinja2

from Clases.Recetas import Receta
from BaseHandler import BaseHandler
from Clases.Usuarios import Usuario
from google.appengine.ext import ndb


template_dir = os.path.join(os.path.dirname(__file__), 'Paginas')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(BaseHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class RegisterHandler(Handler):
    def get(self):
        rol = self.session.get('rol')
        if not rol:
            rol = "Anonimo"
        if rol == "Anonimo":
            self.write("No tienes permiso")
        else:
            self.render_upload("preguntaformulario.html", rol=rol, login='si')
