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
    def get(self, tema="", enunciado="", opc1="", opc2="",opc3="",respcorrecta=""):

        self.write(render_str("insertarpreguntas.html", rol="Anonimo", login="no") % {"tema" :tema,
        "enunciado" : preg_enunciado,
        "opc1" : opc1,
        "opc2" : opc2,
        "opc3" : opc3,
        "respcorrecta" : respcorrecta}
        )


    def post(self):

            preg_tema = self.request.get('tema')
            preg_enunciado = self.request.get('pregunta')
            opc1 = self.request.get('opc.1')
            opc2 = self.request.get('opc.2')
            opc3 = self.request.get('opc.3')
            respcorrecta= self.request.get('respcorrecta')

            sani_tema = escape_html(preg_tema)
            sani_enunciado = escape_html(preg_enunciado)
            sani_opc1 = escape_html(opc1)
            sani_opc2 = escape_html(opc2)
            sani_opc3 = escape_html(opc3)
            sani_respcorrecta = escape_html(respcorrecta)
            errores=""

            usuario = self.session.get('username')
            u = Usuario.query(Usuario.nick == usuario).fetch()[0]
           
            if not tema != "" and pregunta != "" and opc1!="" and opc2=""and opc3="" and respcorrecta="":
                p=Pregunta()
                p.get_id()
                pregunta=Pregunta.query(Pregunta.id_pregunta==user_username).count()
                if pregunta==0:
                   p.id_pregunta=p.get_id()
                   p.tema=preg_tema
                   p.enunciado=preg_enunciado
                   p.solucion=respcorrecta
                   p.respuesta=opc1
                   p.respuesta2=opc2
                   p.respuesta3=opc3
                   u.addpregunta(p)
                    self.render("errores.html", rol='Usuario', login='no', message='Usuario creado correctamente',)
                else:
                    self.write(render_str("insertarpreguntas.html", rol="Anonimo", login="no") % {"tema" :tema,
                    "enunciado" : preg_enunciado,
                    "opc1" : opc1,
                    "opc2" : opc2,
                    "opc3" : opc3,
                    "respcorrecta" : respcorrecta}) p = Pregunta.get_by_id(int(receta_key))
               

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
            self.render_upload("insertarpreguntas.html", rol=rol, login='si')

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/pregunta/addpregunta', AddPregunta),
    ('/iniciosesion', InicioSesion),
    ('/cerrarsesion', CerrarSesion),
    ('/buscar', BuscarPregunta)
],config=config, debug=True)
