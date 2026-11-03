# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def plantillas():

    def GET(id=None, search=None):
        if id:
            fields = [
                db.plantilla.id,
                db.plantilla.texto,
                db.plantilla.modified_by,
                db.plantilla.modified_on,
            ]
            plantilla = db(db.plantilla.id == id).select(*fields).first()
            plantilla.modified_by = plantilla.modified_by and db.vw_usuario(plantilla.modified_by).name
            return response.json(plantilla)

        fds = [
            db.vw_plantilla.id,
            db.vw_plantilla.texto,
            db.vw_plantilla.modified_by,
        ]
        args = dict(distinct=True, orderby=~db.vw_plantilla.id)
        query = db.vw_plantilla.id > 0
        if search:
            query &= db.vw_plantilla.texto.contains(search)
        res = db(query).select(*fds, **args)
        return response.json(res)

    def POST(**vars):
        res = db.plantilla.validate_and_insert(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        plantilla = db.vw_plantilla(res.id)
        return response.json(plantilla)

    # @auth.requires_membership('administrador')
    def PUT(id, **vars):
        res = db(db.plantilla.id == id).validate_and_update(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        return response.json(db.vw_plantilla(id))

    # @auth.requires_membership("administrador")
    def DELETE(id):
        res = db(db.plantilla.id == id).delete()
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
