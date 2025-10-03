# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def suscriptores_():

    def GET(id=None, **vars):
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
            grupo["suscriptores"] = suscriptores()
            grupo["children"] = grupos()
            grupo["notifica"] = notifica()
            return response.json(grupo)
        else:
            from gluon.storage import Storage
            from applications.sms.modules.db.config import grupos

            return response.json(grupos(db, auth, Storage(vars)))

    @auth.requires_login()
    def DELETE(id, **vars):
        res = db(db.grupo.id == id).delete()
        return response.json(res)

    @auth.requires_login()
    def PUT(id, **vars):
        res = db(db.grupo.id == id).validate_and_update(**vars)
        return response.json(res)

    @auth.requires_login()
    def POST(*args, **vars):
        res = db.grupo.validate_and_insert(**vars)
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def suscriptores():

    def GET(id=None, **vars):
        def name(user):
            if not user:
                return ""
            return "{first_name} {last_name}".format(**user).strip()

        if id:
            res = db.suscriptor(id)
            res["grupo"] = db.grupo(res["grupo"])
            res["suplente"] = db.suscriptor(res["suplente"])
            res["created_by"] = name(db.auth_user(res["created_by"]))
            res["modified_by"] = name(db.auth_user(res["modified_by"]))
            return response.json(res)
        else:
            from gluon.storage import Storage
            from applications.sms.modules.db.config import suscriptores

            return response.json(suscriptores(db, auth, Storage(vars)))

    @auth.requires_login()
    def DELETE(id, **vars):
        res = db(db.suscriptor.id == id).delete()
        return response.json(res)

    @auth.requires_login()
    def PUT(id, **vars):
        current_values = (
            db(db.suscriptor.id == id).select(db.suscriptor.telefono).first()
        )

        # `telefono`, fails to update with same value,
        # due to field restriction NOT_IN_DB
        if ("telefono" in vars) and vars["telefono"] == current_values.telefono:
            del vars["telefono"]

        res = db(db.suscriptor.id == id).validate_and_update(**vars)
        return response.json(res)

    @auth.requires_login()
    def POST(*args, **vars):
        res = db.suscriptor.validate_and_insert(**vars)
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
