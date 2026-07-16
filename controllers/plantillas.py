# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def plantillas():

    def GET(id=None, search=None):
        if id:
            def name(user):
                if not user:
                    return ""
                return "{first_name} {last_name}".format(**user).strip()

            fields = [
                db.plantilla.id,
                db.plantilla.texto,
                db.plantilla.created_by,
                db.plantilla.modified_by,
                db.plantilla.created_on,
                db.plantilla.modified_on,
            ]
            row = db(db.plantilla.id == id).select(*fields).first()
            row["created_by"] = name(db.auth_user(row["created_by"]))
            row["modified_by"] = name(db.auth_user(row["modified_by"]))
            return response.json(row)
        else:
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
