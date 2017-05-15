import webapp2
from google.appengine.ext import ndb


class Pregunta(ndb.Model):

    # Id del usuario propietario de la pregunta
    id_usuario = ndb.GenericProperty()

    # Id de la pregunta a la que pertenece la pregunta
    id_pregunta = ndb.StringProperty()

    # El tema de la pregunta
    tema = ndb.StringProperty()

    # Enunciado de la pregunta
    enunciado = ndb.StringProperty()

    # Solucion de la pregunta (Opcion correcta)
    solucion = ndb.StringProperty()

    # Opcion 1 de la pregunta
    respuesta = ndb.StringProperty()

    # Opcion 2 de la pregunta
    respuesta2 = ndb.StringProperty()

    # Opcion 3 de la pregunta
    respuesta3 = ndb.StringProperty()

    

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

    def add_pregunta(self, pregunta):

        m = MiPregunta()
        m.id_pregunta=pregunta
        #m.id_usuario=self.get_id()
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