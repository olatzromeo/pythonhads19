import webapp2
import os
import jinja2

from Clases.Preguntas import Pregunta
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

class MainHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')




class AddPregunta(Handler):
    def post(self):
            try:
            tema = self.request.get('tema')
            pregunta = self.request.get('pregunta')
            opc1 = self.request.get('opc.1')
            opc2 = self.request.get('opc.2')
            opc3 = self.request.get('opc.3')
            respcorrecta= self.request.get('respcorrecta')
           
            if tema != "" and pregunta != "" and opc1!="" and opc2=""and opc3="" and respcorrecta="":
                r = Receta.get_by_id(int(receta_key))
                if r:
                    r.insertar_ingrediente(nombre, cantidad, descripcion)
                    self.write("OK")
                else:
                    self.write("ERROR")
            else:
                self.write("ERROR")
        except ValueError:
            self.write(ValueError)


class BuscarPregunta(Handler):


class VisualizarPreguntas(Handler):
    def get(self):
        login = "no"
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        preguntas = Preguntas.query().fetch()
        self.render("mostrarpreguntas.html", rol=rol, login=login, preguntas=preguntas)


class RegisterHandler(Handler):
    def get(self):
        rol = self.session.get('rol')
        if not rol:
            rol = "Anonimo"
        if rol == "Anonimo":
            self.write("No tienes permiso")
        else:
            self.render_upload("preguntaformulario.html", rol=rol, login='si')

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/pregunta/visualizarpreguntas', VisualizarPreguntas),
    ('/iniciosesion', InicioSesion),
    ('/cerrarsesion', CerrarSesion),
    ('/buscar', BuscarPregunta)
],config=config, debug=True)
