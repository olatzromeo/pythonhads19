import cgi
import webapp2
import os
import jinja2
from BaseHandler import BaseHandler
from webapp2_extras import sessions
import session_module
from Clases.Usuarios import Usuario
from google.appengine.ext import db
import hashlib
import uuid

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

class IniciarSesion(Handler):

    def get(self, nickusuario="", passusuario="", nick_error=""):

        if self.session.get('nickusuario'):
            self.render("errores.html", 
                rol='Usuario', 
                login='si',
                message= self.session.get('nickusuario') + ' la sesion ya existe, estas logueado')
        else:
            self.write(render_str("iniciosesion.html", rol='Anonimo', login='no') % {"nickusuario": nickusuario,
                "passusuario": passusuario, "nick_error": nick_error} 
                )

    def post(self):
        
        def escape_html(s):
            return cgi.escape(s, quote=True)

        user_username = self.request.get('nickusuario')
        user_password = self.request.get('passusuario')
        sani_username = escape_html(user_username)
        sani_password = escape_html(user_password)
        nick_error=""
        password_error=" "

        error=False
        if not valid_password(user_password):
            password_error="El password es INCORRECTO."
            error=True

        if not valid_username(user_username):
            nick_error="El Nick es INCORRECTO"
            error=True

       
        hash_object = hashlib.sha512(user_password)
        hex_dig = hash_object.hexdigest()

        user=Usuario.query(Usuario.nick==user_username).filter(Usuario.password==hex_dig).get()     
        if user:
            #Usuario encontrado
            if user.activado:
                #Usuario activado
                self.session['rol'] = user.rol
                self.session['nickusuario'] = sani_username
                self.render("main.html", rol=user.rol, login='si',)
            else:
                #Usuario sin activar
                self.write(render_str("iniciosesion.html", rol='Anonimo', login='no') % {"nickusuario" :sani_username,
                "passusuario" : " ", 
                "nick_error" : "El usuario no esta activado"})
        else:
            #Usuario NO encontrado
            self.write(render_str("iniciosesion.html", rol='Anonimo', login='no') % {"nickusuario" : sani_username, 
                "passusuario" : "" , "nick_error" : "El usuario y/o contrasena no son correctos"})
        

class CerrarSesion(Handler):
  def get(self):
    for k in self.session.keys():
      del self.session[k]
    self.render("cerrarsesion.html", rol='Anonimo', login='no')


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
    ('/iniciosesion', IniciarSesion),
    ('/cerrarsesion', CerrarSesion)
], config=config, debug=True)
