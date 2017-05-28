import webapp2
import os
import jinja2
import re
import cgi
import session_module
import uuid
import hashlib
from BaseHandler import BaseHandler
from webapp2_extras import sessions
from Clases.Usuarios import Usuario
from google.appengine.ext import db

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
            usuariosesion=self.session[k]
            del self.session[k]
        self.render("cerrarsesion.html", rol='Anonimo', login='no', message = usuariosesion,)

class InicioSesion(Handler):

    def write_form(self, username="", passusuario="",
                     username_error="", password_error=""):

        self.response.write(render_str("iniciosesion.html", rol='Anonimo', login='no') %  {"username" :username,"passusuario" : passusuario,"username_error" : username_error,"password_error": password_error})
    
    def get(self):
         self.write_form()
        
    def post(self):
        
        user_username = self.request.get('username')
        user_password = self.request.get('passusuario')
        sani_username = escape_html(user_username)
        sani_password = escape_html(user_password)
        password_error=""

      
        hash_object = hashlib.sha512(user_password)
        hex_dig = hash_object.hexdigest()
        
        user=Usuario.query(Usuario.nick==user_username).filter(Usuario.password==hex_dig).get()
        #Usuario encontrado
        if user:
            self.session['rol'] = user.rol
            self.session['username'] = sani_username
            self.render("main.html", rol=user.rol, login='si', message = sani_username+ "has iniciado sesion correctamente",)                
        else:
            #Usuario NO encontrado
            self.write(render_str("iniciosesion.html",rol='Anonimo', login='no') % {"username" :sani_username, "passusuario" : "",
            "username_error" : "El nombre de usuario y/o contrasena no es correcto, o no esta registrado", "password_error": ""})
                
        
def escape_html(s):
    return cgi.escape(s, quote=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/iniciosesion', InicioSesion),
    ('/cerrarsesion', CerrarSesion)
],config=config, debug=True)
