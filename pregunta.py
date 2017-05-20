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

	def get(self, tema=" ", enunciado=" ", opcion1=" ", opcion2=" ", opcion3=" ", respcorrecta=" ", errores=""):
		self.response.write(
			render_str("insertarpreguntas.html", rol='Usuario', login='si') % {"tema": tema, "enunciado": enunciado, "opcion1": opcion1, "opcion2": opcion2, "opcion3": opcion3, "respcorrecta": respcorrecta, "errores": errores})

	def post(self):

		def escape_html(s):
			return cgi.escape(s, quote=True)

		tema = self.request.get('tema')
		enunciado = self.request.get('enunciado')
		opcion1 = self.request.get('opcion1')
		opcion2 = self.request.get('opcion2')
		opcion3 = self.request.get('opcion3')
		respcorrecta = self.request.get('respcorrecta')
		errores= ""
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
			pregunta = Preguntas.query(Pregunta.id_pregunta == p.id_pregunta).count()
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
			self.write(render_str("insertarpreguntas.html",rol='Usuario', login='si') % {"tema": sani_tema, "enunciado": sani_enunciado,"opcion1": sani_opc1, "opcion2": sani_opc2,"opcion3": sani_opc3,"respcorrecta": sani_respcorrecta,
            "errores" : "Todos los campos deben de ser rellenados para insertar una nueva pregunta"})

class PreguntasAllHandler(Handler):
    def get(self):
        login = "no"
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        preguntas = Pregunta.query().fetch()
        self.render("verpreguntas.html", rol=rol, login=login, preguntas=preguntas)
		
class BusquedaHandler(Handler):
    def get(self):
        login = "no"
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        preguntas=[]
        self.render("busqueda.html", rol=rol, login=login, preguntas=preguntas)

    def post(self):

        buscar = self.request.get('buscar')

        print("este es el buscar :"+buscar)
        if buscar:
            preguntas = buscar_preguntas(buscar)
        else:
            preguntas = []

        respuesta = ""
        pregunta_card = '''
            <div class="col s12 m4">
               
                        <span class="card-title activator grey-text text-darken-4 truncate">Enunciado: %(enunciado)s</span>
                        <span class="card-title activator grey-text text-darken-4 truncate">a)	%(respuesta)s</span>
                        <span class="card-title activator grey-text text-darken-4 truncate">b)	%(respuesta2)s</span>
                        <span class="card-title activator grey-text text-darken-4 truncate">c)	%(respuesta3)s</span>
    <div class="input-field col s12">
    <select>
      <option value="0" >Elige una respuesta</option>
      <option value="1">a)</option>
      <option value="2">b)</option>
      <option value="3">c)</option>
    </select>
    <label>Respuesta</label>
  </div>'''

        for p in preguntas:
            respuesta += pregunta_card % {"enunciado" :p.enunciado, "respuesta" : p.respuesta, "respuesta2": p.respuesta2, "respuesta3": p.respuesta3}

        self.response.out.write(respuesta)

def buscar_preguntas(busqueda):
    resultado = []
    preguntas = Pregunta.query().fetch()
    for p in preguntas:
        if p.tema in busqueda:
            #print(r.enunciado)
            resultado.append(r)
    return resultado
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
	('/pregunta/visualizarpreguntas', PreguntasAllHandler),
	('/pregunta/busqueda', BusquedaHandler)
    # ('/pregunta/crear', RegisterHandler),
    #('/iniciosesion', InicioSesion),
    #('/cerrarsesion', CerrarSesion)
], config=config, debug=True)
