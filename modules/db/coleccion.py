# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


def limitby(vars):
    min, max = vars.limit.split(",")
    return (int(min), int(max))


def mensajes(db, auth, vars):
    left = False
    fds = [
        db.vw_mensaje.id,
        db.vw_mensaje.de,
        db.vw_mensaje.en,
        db.vw_mensaje.texto,
        db.vw_mensaje.continua,
        db.vw_mensaje.previo,
        db.vw_mensaje.subgrupo,
    ]
    args = dict(distinct=True, orderby=db.vw_mensaje.id)
    vars.limit and args.update(limitby=limitby(vars))
    # q = db.vw_mensaje.id > 0
    if vars.continua:
        q = db.vw_mensaje.continua == True
    elif vars.desde and vars.hasta:
        q = db.vw_mensaje.en >= vars.desde
        q &= db.vw_mensaje.en <= vars.hasta + " 23:59:59"
    else:
        q = db.vw_mensaje.id == 0
    # return::
    sql = db(q)._select(*fds, left=left, **args)
    rows = db.executesql(sql)
    sql = db(q)._select(*fds, left=left).split(" FROM ", 1)
    sql = "SELECT COUNT(DISTINCT vw_mensaje.id) FROM " + sql[1]
    count = db.executesql(sql)[0][0]
    return dict(data=rows, total=count)


def notificados(db, auth, vars):
    left = False
    fds = [
        db.vw_envio.suscriptor,
        db.vw_envio.grupo,
    ]
    args = dict(distinct=True, orderby=~db.vw_envio.grupo_id)
    vars.limit and args.update(limitby=limitby(vars))
    q = db.vw_envio.id > 0
    if vars.mensaje_id:
        q &= db.vw_envio.mensaje_id == vars.mensaje_id
    # return::
    sql = db(q)._select(*fds, left=left, **args)
    rows = db.executesql(sql)
    sql = db(q)._select(*fds, left=left).split(" FROM ", 1)
    sql = "SELECT COUNT(DISTINCT vw_envio.id) FROM " + sql[1]
    count = db.executesql(sql)[0][0]
    return dict(data=rows, total=count)


def plantillas(db, auth, vars):
    left = False
    fds = [
        db.vw_plantilla.texto,
        # db.vw_plantilla.modified_by,
    ]
    args = dict(distinct=True, orderby=~db.vw_plantilla.id)
    vars.limit and args.update(limitby=limitby(vars))
    q = db.vw_plantilla.id > 0
    if vars.texto:
        q &= db.vw_plantilla.texto.contains(vars.texto)
    # return::
    sql = db(q)._select(*fds, left=left, **args)
    rows = db.executesql(sql)
    sql = db(q)._select(*fds, left=left).split(" FROM ", 1)
    sql = "SELECT COUNT(DISTINCT vw_plantilla.id) FROM " + sql[1]
    count = db.executesql(sql)[0][0]
    return dict(data=rows, total=count)
