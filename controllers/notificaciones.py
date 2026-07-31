# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def notificaciones():

    def GET(id=None):
        def pendientes():
            query = db.mensaje.continua == True
            return db(query).count()
        
        res = {
            "pendientes": pendientes()
        }
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
