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
from Clases.Usuarios import Anonimo
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


class InsertarPreguntas(Handler):

    def get(self, autor="", tema=" ", enunciado=" ", opcion1=" ", opcion2=" ", opcion3=" ", respcorrecta=" ", errores=""):
        self.response.write(
            render_str("insertarpreguntas.html", rol='Usuario', login='si') % {"autor": autor, "tema": tema, "enunciado": enunciado, "opcion1": opcion1, "opcion2": opcion2, "opcion3": opcion3, "respcorrecta": respcorrecta, "errores": errores})

    def post(self):

        def escape_html(s):
            return cgi.escape(s, quote=True)

        autor=self.session.get('username')
        tema = self.request.get('tema')
        enunciado = self.request.get('enunciado')
        opcion1 = self.request.get('opcion1')
        opcion2 = self.request.get('opcion2')
        opcion3 = self.request.get('opcion3')
        respcorrecta = self.request.get('miSelect')
        errores= ""
        sani_autor=escape_html(autor)
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
            num = Pregunta.query().count() + 1
            p.tema = tema
            p.autor=autor
            p.id_pregunta = "preg%i" %num
            p.id_usuario = u.get_id()
            p.enunciado = enunciado
            p.solucion = respcorrecta
            p.respuesta = opcion1
            p.respuesta2 = opcion2
            p.respuesta3 = opcion3
            p.put()
            self.render("errores.html", rol='Usuario', login='si', message='Pregunta creada correctamente' )

        else:
            self.write(render_str("insertarpreguntas.html",rol='Usuario', login='si') % { "autor": autor, "tema": sani_tema, "enunciado": sani_enunciado,"opcion1": sani_opc1, "opcion2": sani_opc2,"opcion3": sani_opc3,"respcorrecta": sani_respcorrecta,
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

class ComprobarPregunta(Handler):
	def post(self):
		codPreg = self.request.get('codPreg')
		preg = Pregunta.query(Pregunta.id_pregunta == codPreg).get()
		respuesta = self.request.get('selectedOption')
		if respuesta == preg.solucion:
			self.response.out.write('BIEN')
		else:
			self.response.out.write('MAL')
        
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

        resp = ""
        pregunta_card = '''
            <div class="section">
                <div class="row">
                    <div class="card-panel blue lighten-3 col s12 m6 l8">
                        <span style="font-size: 16px; font-weight: bold;">Tema: </span><span>%(tema)s</span><br>
                        <span style="font-size: 16px; font-weight: bold;">Enunciado: </span><span>%(enunciado)s</span><br>
                        <p style="font-size: 16px; font-weight: bold;">Opciones</p>
                        <span style="font-size: 16px; font-weight: bold;">Op1: </span><span> %(respuesta)s</span><br>
                        <span style="font-size: 16px; font-weight: bold;">Op2: </span><span> %(respuesta2)s</span><br>
                        <span style="font-size: 16px; font-weight: bold;">Op3: </span><span> %(respuesta3)s</span><br>
                    </div>
                </div>
            </div>
        '''
        for p in preguntas:
            resp += pregunta_card % {"tema": p.tema, "enunciado" :p.enunciado, "respuesta" : p.respuesta, "respuesta2": p.respuesta2, "respuesta3": p.respuesta3}

        self.response.out.write(resp)

def buscar_preguntas(busqueda):
    resultado = []
    preguntas = Pregunta.query().fetch()
    for p in preguntas:
        if busqueda in p.tema:
            #print(r.enunciado)
            resultado.append(p)
    return resultado

'''class QuizHandler(Handler):

	def get(self):
			nick = self.session.get('nick')
			#rol="Anonimo"
			login="si"
			tema = self.request.get('tema')
			preguntas = Pregunta.query().order(Pregunta.id_pregunta)
			self.render("quiz.html", rol="", login=login, preguntas=preguntas,)
		
   def post(self):
        tema = self.request.get('tema')
        nick = self.session.get('nick')
        preguntas = Pregunta.query(Pregunta.tema==tema).order(Pregunta.id_pregunta)
        acertadas = 0
        falladas = 0

        for p in preguntas:
            user_respuesta = self.request.get(p.id_pregunta)
            if user_respuesta == p.solucion:
                acertadas = acertadas + 1
            else:
                falladas = falladas + 1

        anonimo = Anonimo.query(Anonimo.nick == self.session.get('nick')).get()
        anonimo.fallos = anonimo.fallos + falladas
        anonimo.aciertos = anonimo.aciertos + acertadas
        anonimo.put()
        self.write(render_str("resultados.html", rol="Anonimo", login='no') % { "nick": nick, "tema": tema, "acertadas": acertadas , "falladas": falladas})
'''

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/pregunta/insertarpreguntas', InsertarPreguntas),
    ('/pregunta/visualizarpreguntas', PreguntasAllHandler),
    ('/pregunta/busqueda', BusquedaHandler),
    #('/pregunta/quiz', QuizHandler),
    ('/pregunta/comprobarPregunta', ComprobarPregunta)

], config=config, debug=True)