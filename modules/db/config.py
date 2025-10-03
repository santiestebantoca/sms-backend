# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


def limitby(vars):
    min, max = vars.limit.split(",")
    return (int(min), int(max))


def grupos(db, auth, vars):
    def traversal(id):
        fds = [
            db.grupo.id,
            db.grupo.nombre,
            db.grupo.pertenece,
            db.grupo.label,
        ]  # `pertenece` for back tracking
        _ = db(db.grupo.id == id).select(*fds).first().as_dict()
        q = db.grupo.pertenece == id
        if vars.label:
            q &= db.grupo.label.contains(vars.label)
        __ = db(q).select(db.grupo.id, orderby=db.grupo.id)
        len(__) and _.update(children=[traversal(r.id) for r in __])
        return _

    _list = []
    q = db.grupo.pertenece == None
    if vars.label:
        q &= db.grupo.label.contains(vars.label)
    for r in db(q).select(db.grupo.id, orderby=db.grupo.id):
        _list.append(traversal(r.id))
    return _list


def suscriptores(db, auth, vars):
    left = False
    fds = [
        db.suscriptor.id,
        db.suscriptor.nombre,
        db.suscriptor.telefono,
        db.suscriptor.activo,
        db.suscriptor.correo,
    ]
    args = dict(distinct=True, orderby=db.suscriptor.id)
    vars.limit and args.update(limitby=limitby(vars))
    q = db.suscriptor.id > 0
    if vars.nombre:
        q &= db.suscriptor.nombre.contains(vars.nombre)
    if vars.no_grupo:
        q &= db.suscriptor.grupo == None
    elif vars.grupo:
        q &= db.suscriptor.grupo == vars.grupo
    # return::
    sql = db(q)._select(*fds, left=left, **args)
    rows = db.executesql(sql)
    sql = db(q)._select(*fds, left=left).split(" FROM ", 1)
    sql = "SELECT COUNT(DISTINCT suscriptor.id) FROM " + sql[1]
    count = db.executesql(sql)[0][0]
    return dict(data=rows, total=count)


def users(db, auth, vars):
    """
    returns::
    (admin): all rows from `usuario`
    (admin no AR): rows from `usuario` where
        (`usuario` with same `area` as auth.user) or \
        ((`usuario` has no area) and (`usuario` is created by auth.user))
    """
    left = False
    fds = [
        db.auth_user.id,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.auth_user.username,
        db.auth_user.registration_key,
    ]
    args = dict(distinct=True, orderby=~db.auth_user.id)
    vars.limit and args.update(limitby=limitby(vars))
    q = db.auth_user.id > 0
    # return::
    sql = db(q)._select(*fds, left=left, **args)
    rows = db.executesql(sql)
    sql = db(q)._select(*fds, left=left).split(" FROM ", 1)
    sql = "SELECT COUNT(DISTINCT auth_user.id) FROM " + sql[1]
    count = db.executesql(sql)[0][0]
    return dict(data=rows, total=count)


def plantillas(db, auth, vars):
    left = False
    fds = [
        db.vw_plantilla.id,
        db.vw_plantilla.texto,
        db.vw_plantilla.modified_by,
    ]
    args = dict(distinct=True, orderby=~db.vw_plantilla.id)
    vars.limit and args.update(limitby=limitby(vars))
    q = db.vw_plantilla.id > 0
    # return::
    sql = db(q)._select(*fds, left=left, **args)
    rows = db.executesql(sql)
    sql = db(q)._select(*fds, left=left).split(" FROM ", 1)
    sql = "SELECT COUNT(DISTINCT vw_plantilla.id) FROM " + sql[1]
    count = db.executesql(sql)[0][0]
    return dict(data=rows, total=count)
