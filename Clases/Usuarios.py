import webapp2
from google.appengine.ext import ndb
from Preguntas import Pregunta


class Usuario(ndb.Model):

    # Nick del usuario
    nick = ndb.StringProperty()

    # Nombre del usuario
    name = ndb.StringProperty()

    # Apellido del usuario
    surname = ndb.StringProperty()

    # Password del usuario
    password = ndb.StringProperty()

    # Email del usuario
    email = ndb.StringProperty()

    # Usuario activado o no
    #activado = ndb.BooleanProperty()

    # rol
    rol = ndb.StringProperty()

    # Fecha de registro del usuario
    date = ndb.DateTimeProperty(auto_now_add=True)

    """
        Funcion que devuelve el id del usuario, tipo Long
    """
    def get_id(self):
        return self.key.id()

    """
        Funcion que devuelve el id como string
    """
    def get_id_as_str(self):

        return self.key.id().__str__

    """
        Funcion que devuelve activado
    
    def get_activado(self):

        return self.activado.id()
    """
    def add_pregunta(self, pregunta):

        m = MiPregunta()
        m.id_pregunta=pregunta
        m.id_usuario=self.get_id()
        m.put()

    def del_pregunta(self, pregunta):
        m = MiPregunta.query(MiPregunta.id_usuario == self.get_id()).filter(MiPregunta.id_pregunta == pregunta).fetch()[0]
        m.delete()

    def pregunta_guardada(self,pregunta):
        m = Mipregunta.query(Mipregunta.id_usuario == self.get_id()).filter(Mipregunta.id_pregunta == pregunta).count()
        print("Numero de pregunta" + str(m))
        if m > 0:
            return True
        else:
            return False

    def get_preguntas(self):
        preguntas=[]
        mias = MiPregunta.query(MiPregunta.id_usuario==self.get_id())
        for r in mias:
            preguntas.append(pregunta.get_by_id(int(r.id_pregunta)))
        return preguntas


class MiPregunta(ndb.Model):

    id_pregunta = ndb.GenericProperty()
    id_usuario = ndb.GenericProperty()

    def delete(self):
        self.key.delete()