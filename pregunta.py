import webapp2
import os
import jinja2
import re
import cgi
from BaseHandler import BaseHandler
import uuid
import hashlib
from Clases.Preguntas import Pregunta
from Clases.Usuarios import Usuario
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), 'Paginas')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(BaseHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


'''class MainHandler(Handler):
	def get(self):
		usuario = self.session.get('username')
		rol = self.session.get('rol')'''


class InsertarPreguntas(Handler):

	def get(self, tema="", enunciado="", opcion1="", opcion2="", opcion3="", respcorrecta=""):
		self.response.write(
			render_str("insertarpreguntas.html", rol='Usuario', login='si') % {"tema": tema, "enunciado": enunciado,"opcion1": opcion1, "opcion2": opcion2,"opcion3": opcion3,"respcorrecta": respcorrecta})


	def post(self):

		def escape_html(s):
			return cgi.escape(s, quote=True)

		tema = self.request.get('tema')
		enunciado = self.request.get('enunciado')
		opcion1 = self.request.get('opcion1')
		opcion2 = self.request.get('opcion2')
		opcion3 = self.request.get('opcion3')
		respcorrecta = self.request.get('respcorrecta')
		sani_tema = escape_html(tema)
		sani_enunciado = escape_html(enunciado)
		sani_opc1 = escape_html(opcion1)
		sani_opc2 = escape_html(opcion2)
		sani_opc3 = escape_html(opcion3)
		sani_respcorrecta = escape_html(respcorrecta)

		usuario = self.session.get('username')
		u = Usuario.query(Usuario.nick == usuario).fetch()[0]

		if tema != "" and enunciado != "" and opcion1 != "" and opcion2 != "" and opcion3 != "" and respcorrecta != "":
			p = Pregunta()
			'''p.id_pregunta = p.get_id()
			pregunta = Pregunta.query(Pregunta.id_pregunta == p.id_pregunta).count()
			if  pregunta == 0:'''
			p.tema = tema

			p.id_pregunta = self.request.get('id')
			p.id_usuario = u.get_id()
			p.enunciado = enunciado
			p.solucion = respcorrecta
			p.respuesta = opcion1
			p.respuesta2 = opcion2
			p.respuesta3 = opcion3
			p.put()
			#p.add_pregunta(p)
			self.render("errores.html", rol='Usuario', login='si', message='Pregunta creada correctamente', )

		else:
			self.render("errores.html", rol='Usuario', login='si',
            	message='Todos los campos deben de ser rellenados para insertar una nueva pregunta', )

'''class VisualizarPreguntas(Handler):
	def get(self):
		login = "no"
		usuario = self.session.get('username')
		rol = self.session.get('rol')
		if usuario:
			login = "si"
		if not rol:
			rol = "Anonimo"
		preguntas = Preguntas.query().fetch()
		self.render("visualizarpreguntas.html", rol=rol, login=login, preguntas=preguntas)'''

'''
class RegisterHandler(Handler):
    def get(self):
        rol = self.session.get('rol')
        if not rol:
            rol = "Anonimo"
        if rol == "Anonimo":
            self.write("No tienes permiso")
        else:
            self.render_upload("insertarpreguntas.html", rol=rol, login='si')
'''

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/pregunta/insertarpreguntas', InsertarPreguntas),
    # ('/pregunta/crear', RegisterHandler),
    #('/iniciosesion', InicioSesion),
    #('/cerrarsesion', CerrarSesion)
], config=config, debug=True)
