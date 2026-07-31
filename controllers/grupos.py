# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def grupos():

    def GET(id=None, label='all', pertenece=None, include=None):
        if id:
            # def suscriptores():
            #     q = db.suscriptor.grupo == id
            #     return db(q).select(orderby=db.suscriptor.id).as_list()

            # def grupos():
            #     q = db.grupo.pertenece == id
            #     return db(q).select(orderby=db.grupo.id).as_list()

            # def notificados():
            #     q = db.vw_notifica.grupo_a == id
            #     return db(q).select(orderby=db.vw_notifica.id).as_list()

            grupo = db.grupo(id)
            if not grupo:
                response.status = 404
                return response.json(None)
            # if include == 'all':
            #     grupo["suscriptores"] = suscriptores()
            #     grupo["hijos"] = grupos()
            #     grupo["notificados"] = notificados()
            
            return response.json(grupo)
        else:
            q = db.grupo.id > 0
            if 'grupo' in label and 'centro' in label:
                q &= ((db.grupo.label == None) | db.grupo.label.contains('centro'))
            if 'centro' in label and 'origen' in label:
                q &= db.grupo.label.contains(['centro', 'origen'])
            if pertenece:
                q &= db.grupo.pertenece == pertenece
            res = db(q).select(orderby=db.grupo.id)
            return response.json(res)             

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
