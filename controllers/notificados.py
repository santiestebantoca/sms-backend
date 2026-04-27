# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def notificados():

    def GET(id=None, origen=None, include=None):
        def ids():
            q = db.notifica.grupo_a.belongs(origen.split(","))
            return db(q)._select(db.notifica.grupo_b)

        if origen:
            fds = [
                db.grupo.id,
                db.grupo.nombre,
                db.grupo.apodo
            ]
            args = dict(orderby=db.grupo.id)
            query = db.grupo.id.belongs(ids())
            res = db(query).select(*fds, **args)
            if include == 'suscriptor':
                fds = [
                    db.suscriptor.id,
                    db.suscriptor.nombre,
                    db.suscriptor.cargo,
                    db.suscriptor.telefono,
                    db.suscriptor.grupo,
                ]
                for r in res:
                    r.update(suscriptores=(
                        db(db.suscriptor.grupo == r["id"]).select(
                            *fds).as_list()
                    ))
            return response.json(res)
        else:
            return response.json([])

    @auth.requires_login()
    def POST(grupo_a, grupo_b):
        db(db.notifica.grupo_a == grupo_a).delete()
        data = [{"grupo_a": grupo_a, "grupo_b": val} for val in grupo_b]
        res = db.notifica.bulk_insert(data)  # [1, 2, ...]
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
