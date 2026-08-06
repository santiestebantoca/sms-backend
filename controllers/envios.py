# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def envios():

    def GET(id=None, mensaje_id=None):
        fds = [
            db.vw_envio.suscriptor_id,
            db.vw_envio.suscriptor,
            db.vw_envio.grupo,
        ]
        args = dict(distinct=True, orderby=~db.vw_envio.grupo_id)
        query = db.vw_envio.mensaje_id == mensaje_id
        res = db(query).select(*fds, **args)
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()

