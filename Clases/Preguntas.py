import webapp2
from google.appengine.ext import ndb


class Pregunta(ndb.Model):

    # Id del usuario propietario de la pregunta
    id_usuario = ndb.GenericProperty()

    # Id de la pregunta a la que pertenece la pregunta
    id_pregunta = ndb.StringProperty()

    # El tema de la pregunta
    tema = ndb.IntegerProperty()

    # Enunciado de la pregunta
    enunciado = ndb.StringProperty()

    # Solucion de la pregunta (Opcion correcta)
    solucion = ndb.StringProperty()

    # Opcion 1 de la pregunta
    respuesta = ndb.StringProperty()

    # Opcion 2 de la pregunta
    respuesta2 = ndb.BlobKeyProperty()

    # Opcion 3 de la pregunta
    respuesta3 = ndb.IntegerProperty()

    

    def delete(self):
        return self.key.delete()

    """
        Funcion para obtener directamente el id del objeto
    """
    def get_id(self):

        return self.key.id()

    """
        Funcion para insertar una pregunta
    """
    def insertar_pregunta(self, id_autor, tema, enunciado,respuesta,respuesta2,respuesta3,respuestacorrecta):
        p = Pregunta(id_usuario=id_autor,id_pregunta=self.get_id(),tema=tema,enunciado=enunciado,solucion=respuestacorrecta,respuesta=respuesta,respuesta2=respuesta2,respuesta3=respuesta3)
        p.put()
