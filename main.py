import cgi
import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from Clases.Usuarios import Anonimo

from session_module import BaseSessionHandler


##################################JINJA2##############################################
template_dir = os.path.join(os.path.dirname(__file__), 'Paginas')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Handler(BaseSessionHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class MainHandler(Handler):
    def write_main(self, last_nick="", aciertos="", total="", onload="", nick="", nick_error=""):
        self.render("index.html", nick=last_nick, aciertos=aciertos, total=total)

    def get(self):
        usuario=self.session.get('nick')
        rol=self.session.get('rol')
        login="no"
        if usuario:
            login="si"
        if not rol:
            rol="Anonimo"
        self.render("index.html", rol=rol, login=login)

    def post(self):
        def escape_html(s):
            return cgi.escape(s, quote=True)

        anonimo_nick = self.request.get('nick')
        sani_nick = escape_html(anonimo_nick)
        nick_error = ""

        error = False
        if not anonimo_nick:
            nick_error = "Debes introducir un nick"
            error = True

        if error:
            self.write_main("", "", "", "", anonimo_nick, nick_error)
        else:
            anonimo = Anonimo.query(Anonimo.nick == anonimo_nick).count()
            if anonimo == 0:
                a = Anonimo()
                a.nick = anonimo_nick
                a.aciertos = 0
                a.fallos = 0
                a.put()
                rol="Anonimo"
                login="si"
                self.session['Anonimo'] = anonimo_nick
                self.render("preguntas.html", rol=rol, login=login)
            else:
                rol="Anonimo"
                login="si"
                self.session['Anonimo'] = anonimo_nick
                self.render("preguntas.html", rol=rol, login=login)

class InicioSesionHandler(Handler):
    def get(self):
        usuario = self.session.get('nickusuario')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("iniciosesion.html", rol=rol, login=login)

class RegistroHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("registro.html", rol=rol, login=login)

class PreguntaHandler(Handler):
      def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("preguntas.html", rol=rol, login=login)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([  
	('/', MainHandler),
    ('/iniciosesion', InicioSesionHandler),
    ('/registro', RegistroHandler),
    ('/pregunta', PreguntaHandler),

], config=config, debug=True)

   