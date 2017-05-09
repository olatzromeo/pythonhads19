import webapp2
import os
import jinja2
import re
import cgi
import session_module
from BaseHandler import BaseHandler
from webapp2_extras import sessions
from Clases.Usuarios import Usuario
from google.appengine.ext import db
import uuid
import hashlib

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

class CerrarSesion(Handler):
    def get(self):
        for k in self.session.keys():
            del self.session[k]
        self.render("cerrarsesion.html", rol='Anonimo', login='no')

class InicioSesion(Handler):

    def get(self, username="", passusuario="",username_error=""):

        if self.session.get('username'):
            self.render("errores.html", rol='Usuario', login='si', message= self.session.get('username') + "ya has iniciado antes la sesion",)
        else:
            self.write(render_str("iniciosesion.html",rol='Anonimo', login='no') % {"username" :username,
                "passusuario" : passusuario,
                "username_error" : username_error})

    def post(self):
        
        def escape_html(s):
            return cgi.escape(s, quote=True)

        user_username = self.request.get('username')
        user_password = self.request.get('passusuario')
        sani_username = escape_html(user_username)
        sani_password = escape_html(user_password)

        hash_object = hashlib.sha512(user_password)
        hex_dig = hash_object.hexdigest()

        user=Usuario.query(Usuario.nick==user_username).filter(Usuario.password==hex_dig).get()
        if user:
            #Usuario encontrado
            if user.activado:
                #Usuario activado
                self.session['rol'] = user.rol
                self.session['username'] = sani_username
                self.render("main.html", rol=user.rol, login='si', message = sani_username+"has iniciado sesion correctamente" ,)
            else:
                #Usuario esta activado
                self.write(render_str("iniciosesion.html", rol='Anonimo', login='no') % {"username" :sani_username,
                "passusuario" : "",
                "username_error" : "El usuario no esta activado"})

        else:
            #Usuario NO encontrado
            self.write(render_str("login.html",rol='Anonimo', login='no') % {"username" :sani_username,
            "passusuario" : "",
            "username_error" : "El nombre de usuario y/o contrasena no es correcto"})


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/iniciosesion', InicioSesion),
    ('/cerrarsesion', CerrarSesion)
],config=config, debug=True)
