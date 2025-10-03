# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def plantillas():

    def GET(id=None, **vars):
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
            from gluon.storage import Storage
            from applications.sms.modules.db.config import plantillas

            return response.json(plantillas(db, auth, Storage(vars)))

    # @auth.requires_membership('administrador')
    def POST(*args, **vars):
        res = db.plantilla.validate_and_insert(**vars)
        return response.json(res)

    # @auth.requires_membership('administrador')
    def PUT(id, **vars):
        res = db(db.plantilla.id == id).validate_and_update(**vars)
        return response.json(res)

    # @auth.requires_membership("administrador")
    def DELETE(id, **vars):
        res = db(db.plantilla.id == id).delete()
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
