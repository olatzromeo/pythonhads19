import webapp2
from google.appengine.ext import ndb


class Pregunta(ndb.Model):

    # Id del usuario propietario de la pregunta
    id_usuario = ndb.GenericProperty()

    # Id de la categoria a la que pertenece la pregunta
    id_categoria = ndb.StringProperty()

    # Nombre de la pregunta
    nombre = ndb.StringProperty()

    # Solucion de la pregunta
    solucion = ndb.StringProperty()

    # Etiquetas de la pregunta
    respuesta = ndb.StringProperty()

    # Clave para buscar la foto
    respuesta2 = ndb.BlobKeyProperty()

    # Para controlar el numero de pasos
    respuesta3 = ndb.IntegerProperty()

    # Para controlar el numero de votos
    tema = ndb.IntegerProperty()

    def delete(self):
        return self.key.delete()

    """
        Funcion para obtener directamente el id del objeto
    """
    def get_id(self):

        return self.key.id()