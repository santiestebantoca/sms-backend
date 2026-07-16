# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def suscriptores():
    
    def GET(id=None):
        if id:
            res = db.suscriptor(id)
            return response.json(res)
    
    @auth.requires_login()
    def DELETE(id):
        res = db(db.suscriptor.id == id).delete()
        return response.json(res)

    @auth.requires_login()
    def PUT(id, **vars):
        otros_suscriptores = db(db.suscriptor.id != id)
        db.suscriptor.telefono.requires = IS_NOT_IN_DB(otros_suscriptores, "suscriptor.telefono")            
        res = db(db.suscriptor.id == id).validate_and_update(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        return response.json(db.suscriptor(id))

    @auth.requires_login()
    def POST(**vars):
        res = db.suscriptor.validate_and_insert(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        return response.json(db.suscriptor(res.id))

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
