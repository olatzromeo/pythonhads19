import cgi
import os
import webapp2
import jinja2
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
    def get(self):
        usuario=self.session.get('nickusuario')
        rol=self.session.get('rol')
        login="no"
        if usuario:
            login="si"
        if not rol:
            rol="Anonimo"
        self.render("main.html", rol=rol, login=login)

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


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([  
	('/', MainHandler),
    ('/iniciosesion', InicioSesionHandler),
    ('/registro', RegistroHandler)
], config=config, debug=True)

   