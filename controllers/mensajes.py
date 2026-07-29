# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


@request.restful()
def notificaciones():

    def GET(id=None):
        def pendientes():
            query = db.mensaje.continua == True
            return db(query).count()
        
        res = {
            "pendientes": pendientes()
        }
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def mensajes():

    def GET(id=None, continua=None, desde=None, hasta=None, search=None, include=None):
        if id:
            def suscriptores(mensaje_id):
                fds = [
                    db.vw_envio.suscriptor_id,
                    db.vw_envio.suscriptor,
                    db.vw_envio.grupo
                ]
                args = dict(distinct=True, orderby=~db.vw_envio.grupo_id)
                query = db.vw_envio.mensaje_id == mensaje_id
                return db(query).select(*fds, **args).as_list()

            res = db.mensaje(id)
            _include = include.split(",") if include else []
            if "destinatarios" in _include:
                res["destinatarios"] = suscriptores(id)
            return response.json(res)
        else:
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
            query = None
            if continua:
                query = db.vw_mensaje.continua == True
            elif desde and hasta:
                query = db.vw_mensaje.en >= desde
                query &= db.vw_mensaje.en <= hasta + " 23:59:59"
            if query:
                if search:
                    query &= db.vw_mensaje.texto.contains(search)
            else:
                query = db.vw_mensaje.id == 0
            res = db(query).select(*fds, **args)
            return response.json(res)

    @auth.requires_login()
    def PUT(id, **vars):
        res = db(db.mensaje.id == id).validate_and_update(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        return response.json(db.mensaje(id))

    @auth.requires_login()
    def POST(**vars):
        """
        vars (texto, continua, previo, destinatarios)
        """
        from applications.sms.modules.notificar.notificar import notificar

        query = db.suscriptor.id.belongs(vars["destinatarios"])
        suscriptores = db(query).select()
        res = db.mensaje.validate_and_insert(de=auth.user_id,
                                             texto=vars["texto"],
                                             continua=vars["continua"],
                                             previo=vars["previo"])
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        mensaje = db.mensaje(res.id)
        if mensaje.previo:
            previo = db.mensaje(mensaje.previo)
            previo.update_record(continua=False)
            mensaje.update_record(subgrupo=previo.subgrupo or previo.id)
        else:
            mensaje.update_record(subgrupo=mensaje.id)
        for suscriptor in suscriptores:
            res = db.envio.validate_and_insert(mensaje_id=mensaje.id,
                                               suscriptor_id=suscriptor.id)
            notificar(suscriptor, mensaje.texto, db_smsgw=db_smsgw, mail_obj=mail)
            
        return response.json(mensaje)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()
