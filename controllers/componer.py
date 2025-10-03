# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def grupos():

    def GET(id=None, **vars):
        from gluon.storage import Storage
        from applications.sms.modules.db.componer import grupos

        return response.json(grupos(db, auth, Storage(vars)))

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def notificados():

    def GET(id=None, **vars):
        from gluon.storage import Storage
        from applications.sms.modules.db.componer import notificados

        return response.json(notificados(db, Storage(vars)))

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def previo():

    def GET(id=None, **vars):

        def notificados():
            fds = [
                db.vw_envio.suscriptor_id,
                db.vw_envio.suscriptor,
                db.vw_envio.grupo,
            ]
            args = dict(orderby=~db.vw_envio.grupo_id)
            q = db.vw_envio.mensaje_id == id
            return db(q).select(*fds, **args).as_list()

        res = db.mensaje(id)
        res["notificados"] = notificados()

        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
