# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


# def grupos(db, auth, vars):
#     def traversal(id):
#         fds = [
#             db.grupo.id,
#             db.grupo.nombre,
#             db.grupo.apodo,
#             db.grupo.pertenece,
#             db.grupo.label,
#         ]  # `pertenece` for back tracking
#         _ = db(db.grupo.id == id).select(*fds).first().as_dict()
#         q = db.grupo.pertenece == id
#         if vars.label:
#             q &= db.grupo.label.contains(vars.label)
#         __ = db(q).select(db.grupo.id, orderby=db.grupo.id)
#         len(__) and _.update(children=[traversal(r.id) for r in __])
#         return _

#     _list = []
#     q = db.grupo.pertenece == None
#     if vars.label:
#         q &= db.grupo.label.contains(vars.label)
#     for r in db(q).select(db.grupo.id, orderby=db.grupo.id):
#         _list.append(traversal(r.id))
#     return _list


# def notificados(db, vars):
#     def ids():
#         q = db.notifica.grupo_a.belongs(vars.grupo.split(","))
#         return db(q)._select(db.notifica.grupo_b)

#     if vars.grupo:
#         fds = [db.grupo.id, db.grupo.nombre, db.grupo.apodo]
#         q = db.grupo.id.belongs(ids())
#         rs = db(q).select(*fds).as_list()
#         fds = [
#             db.suscriptor.id,
#             db.suscriptor.nombre,
#             db.suscriptor.cargo,
#             db.suscriptor.telefono,
#             db.suscriptor.grupo,
#         ]
#         for r in rs:
#             r["suscriptores"] = (
#                 db(db.suscriptor.grupo == r["id"]).select(*fds).as_list()
#             )
#         # return::
#         return rs
#     else:
#         return []


def suscriptores(db, vars):
    fds = [
        db.suscriptor.id,
        db.suscriptor.nombre,
        db.suscriptor.cargo,
        db.suscriptor.telefono,
        db.suscriptor.grupo,
    ]
    args = dict(orderby=db.suscriptor.nombre)
    q = db.suscriptor.id > 1
    if vars["grupo[]"]:
        q &= db.suscriptor.grupo.belongs(vars["grupo[]"])
    # return::
    return db(q).select(*fds, **args).as_list()
