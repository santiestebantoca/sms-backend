# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def notificados():

    def GET(id=None, origen=None, include=None):
        def grupos_notificados_ids(grupo_a_ids):
            q = db.notifica.grupo_a.belongs(grupo_a_ids)
            return db(q)._select(db.notifica.grupo_b)

        if origen:
            origenes = origen if isinstance(origen, list) else [origen]
            fds = [
                db.grupo.id,
                db.grupo.nombre,
                db.grupo.apodo
            ]
            args = dict(orderby=db.grupo.id)
            query = db.grupo.id.belongs(grupos_notificados_ids(origenes))
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
    def PUT(grupo_a, grupo_b):
        # 1. Eliminar los que ya no están
        deleteQuery = db.notifica.grupo_a == grupo_a
        deleteQuery &= ~db.notifica.grupo_b.belongs(grupo_b)
        db(deleteQuery).delete()

        # 2. Crear los nuevos (bulk)
        existentes = db(db.notifica.grupo_a == grupo_a).select(
            db.notifica.grupo_b)
        existentes_set = set(row.grupo_b for row in existentes)

        nuevos = [{'grupo_a': grupo_a, 'grupo_b': b}
                  for b in grupo_b if b not in existentes_set]
        if nuevos:
            db.notifica.bulk_insert(nuevos)

        # 3. Devolver los registros existentes después del PUT
        res = db(db.notifica.grupo_a == grupo_a).select()

        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
