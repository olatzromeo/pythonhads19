import webapp2
import os
import jinja2
import re
import cgi
from BaseHandler import BaseHandler
import uuid
import hashlib
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


class Registro(Handler):

    def get(self, username="", password="", verify="",email="", username_error="", password_error="",verify_error="", email_error="",name="",surname="",name_error="",surname_error=""):

        self.write(render_str("registro.html", rol="Anonimo", login="no") % {"username" :username,
        "password" : password,
        "verify" : verify,
        "email" : email,
        "name" : name,
        "surname" : surname,
        "username_error" : username_error,
        "password_error" : password_error,
        "verify_error" : verify_error,
        "email_error" : email_error,
        "name_error" : name_error,
        "surname_error" : surname_error}
        )

    def post(self):
        ## VALIDACIONES##
        def escape_html(s):
            return cgi.escape(s, quote=True)

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        NOMBRE_RE = re.compile(r"^[a-zA-Z-]{3,30}$")

        def valid_username(username):
            return USER_RE.match(username)

        def valid_password(password):
            return PASSWORD_RE.match(password)

        def valid_email(email):
            return EMAIL_RE.match(email)

        def valid_name(nombre):
            return NOMBRE_RE.match(nombre)

        def hash_password(password):
            hash_object = hashlib.sha512(user_password)
            hex_dig = hash_object.hexdigest()
            return hex_dig

        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
        user_name = self.request.get('name')
        user_surname = self.request.get('surname')
        sani_username = escape_html(user_username)
        sani_password = escape_html(user_password)
        sani_verify = escape_html(user_verify)
        sani_email = escape_html(user_email)
        sani_name = escape_html(user_name)
        sani_surname = escape_html(user_surname)
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""
        name_error = ""
        surname_error = ""

        error = False
        if not valid_username(user_username):
            username_error = "Usuario incorrecto! "
            error = True
        if not valid_password(user_password):
            password_error = "Password incorrecto!"
            error = True
        if not user_verify or not user_password == user_verify:
            verify_error = "Password no coincide!"
            error = True
        if not valid_email(user_email):
            email_error = "Email incorrecto!"
            error = True
        if not valid_name(user_name):
            name_error = "Nombre incorrecto!"
            error = True
        if not valid_name(user_surname):
            surname_error = "Apellido incorrecto!"
            error = True

        if error:
            self.write(render_str("registro.html", rol="Anonimo", login="no") % {"username" :sani_username,
            "password" : sani_password,
            "verify" : sani_verify,
            "email" : sani_email,
            "name" : sani_name,
            "surname" : sani_surname,
            "username_error" : username_error,
            "password_error" : password_error,
            "verify_error" : verify_error,
            "email_error" : email_error,
            "name_error" : name_error,
            "surname_error" : surname_error})
        else:
            user=Usuario.query(Usuario.nick==user_username).count()
            if user==0:
                u=Usuario()
                u.nick=user_username
                u.email=user_email
                u.password = hash_password(user_password)
                u.name= user_name
                u.surname = user_surname
                u.activado = False
                u.rol = "Usuario"
                u.put()
                self.render("errores.html", rol='Usuario', login='no', message='Usuario creado correctamente',)
            else:
                self.write(render_str("registro.html") % {"username" :sani_username,
                "password" : sani_password,
                "verify" : sani_verify,
                "email" : sani_email,
                "name" : sani_name,
                "surname" : sani_surname,
                "username_error" : "Nick actualmente en uso",
                "password_error" : password_error,
                "verify_error" : verify_error,
                "email_error" : email_error,
                "name_error" : name_error,
                "surname_error" : surname_error})


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/registro', Registro)
    ], config=config, debug=True)
