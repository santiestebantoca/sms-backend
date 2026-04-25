# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def grupos():

    def GET(id=None, label=None, include=None):
        if id:
            def suscriptores():
                q = db.suscriptor.grupo == id
                return db(q).select(orderby=db.suscriptor.id).as_list()

            def grupos():
                q = db.grupo.pertenece == id
                return db(q).select(orderby=db.grupo.id).as_list()

            def notifica():
                q = db.vw_notifica.grupo_a == id
                return db(q).select(orderby=db.vw_notifica.id).as_list()

            grupo = db.grupo(id)
            if not grupo:
                response.status = 404
                return response.json(None)
            _include = include.split(",") if include else []
            if "suscriptores" in _include:
                grupo["suscriptores"] = suscriptores()
            if "hijos" in _include:
                grupo["children"] = grupos()
            if "notificados" in _include:
                grupo["notifica"] = notifica()
            return response.json(grupo)
        else:
            def traversal(id):
                fds = [
                    db.grupo.id,
                    db.grupo.nombre,
                    db.grupo.apodo,
                    db.grupo.pertenece,
                    db.grupo.label,
                ]  # `pertenece` for back tracking
                _ = db(db.grupo.id == id).select(*fds).first().as_dict()
                q = db.grupo.pertenece == id
                if label:
                    q &= db.grupo.label.contains(label)
                __ = db(q).select(db.grupo.id, orderby=db.grupo.id)
                len(__) and _.update(children=[traversal(r.id) for r in __])
                return _

            _list = []
            q = db.grupo.pertenece == None
            if label:
                q &= db.grupo.label.contains(label)
            for r in db(q).select(db.grupo.id, orderby=db.grupo.id):
                _list.append(traversal(r.id))
            return response.json(_list)

    @auth.requires_login()
    def DELETE(id):
        res = db(db.grupo.id == id).delete()
        return response.json(res)

    @auth.requires_login()
    def PUT(id, **vars):
        otros_grupos = db(db.grupo.id != id)
        db.grupo.apodo.requires = IS_EMPTY_OR(
            IS_NOT_IN_DB(otros_grupos, "grupo.apodo", error_message="Ya existe el alias"))
        res = db(db.grupo.id == id).validate_and_update(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        return response.json(db.grupo(id))

    @auth.requires_login()
    def POST(**vars):
        res = db.grupo.validate_and_insert(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        return response.json(db.grupo(res.id))

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
