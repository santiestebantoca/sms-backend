# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def mensajes():

    def GET(id=None, **vars):
        if id:
            pass
        else:
            from gluon.storage import Storage
            from applications.sms.modules.db.coleccion import mensajes

            return response.json(mensajes(db, auth, Storage(vars)))

    @auth.requires_login()
    def PUT(id, **vars):
        res = db(db.mensaje.id == id).validate_and_update(**vars)
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def notificados():

    def GET(id=None, **vars):
        from gluon.storage import Storage
        from applications.sms.modules.db.coleccion import notificados

        return response.json(notificados(db, auth, Storage(vars)))

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def nav():

    def GET(id=None, **vars):
        res = db(db.mensaje.continua == True).count()
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def plantillas():

    def GET(*args, **vars):
        from gluon.storage import Storage
        from applications.sms.modules.db.coleccion import plantillas

        return response.json(plantillas(db, auth, Storage(vars)))

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
