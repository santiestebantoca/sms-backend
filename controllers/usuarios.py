# -*- coding: utf-8 -*-
__author__ = 'jorge.santiesteban'


@request.restful()
def usuarios():
    
    @auth.requires_membership('administrador')
    def GET(id=None, search=None):
        if id:
            grupos_ids = db(db.auth_membership.user_id == id)._select(db.auth_membership.group_id)
            # Tiene que ser auth_user, no vw_usuario, para formulario editar (fisrt_name, ...)
            fds = [
                db.auth_user.id,
                db.auth_user.first_name,
                db.auth_user.last_name,
                db.auth_user.username,
                db.auth_user.registration_key,
                db.auth_user.modified_on,
                db.auth_user.modified_by,
            ]
            usuario = db(db.auth_user.id == id).select(*fds).first()
            usuario.grupos = db(db.auth_group.id.belongs(grupos_ids)).select().as_list()
            usuario.modified_by = usuario.modified_by and db.vw_usuario(usuario.modified_by).name
            return response.json(usuario)

        fds = [
            db.vw_usuario.id,
            db.vw_usuario.name,
            db.vw_usuario.registration_key,
        ]
        args = dict(distinct=True, orderby=db.vw_usuario.name)
        query = db.vw_usuario.id > 0
        if search:
            query &= db.vw_usuario.name.contains(search)
        res = db(query).select(*fds, **args)
        return response.json(res)
            
    @auth.requires_membership('administrador')
    def POST(grupos, **vars):
        """
        Auth valida:
        1. `email` y `username` no vacíos y no tomados.
        2. `password` no vacío.
        Auth establece por defecto:
        1. `registration_key`, `reset_password_key`, `registration_id` en '' (vacío).
        Reglas:
        1. Se disabilita la validación de `password` (No viene en vars).
        2. Se disabilita la validación de `email` (No viene en vars / no se usa en esta app).
        3. Se establecen `registration_key`, `reset_password_key`, `registration_id` en None (NULL).
        """
        db.auth_user.password.requires = None
        db.auth_user.email.requires = None
        db.auth_user.registration_key.default = None
        db.auth_user.reset_password_key.default = None
        db.auth_user.registration_id.default = None
        res = db.auth_user.validate_and_insert(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        # Membership
        from applications.sms.modules.db.auth import create_membership
        
        create_membership(res.id, grupos)

        return response.json(db.auth_user(res.id))
    
    @auth.requires_login()
    def PUT(id, grupos, **vars):
        """
        Reglas:
        1. Se disabilita la validación de `email` (No viene en vars / no se usa en esta app).
        2. Se valida `username` no vacío y no tomado.
        """
        db.auth_user.email.requires = None
        otros_usuarios = db(db.auth_user.id != id)
        db.auth_user.username.requires = [
            IS_NOT_EMPTY(),
            IS_NOT_IN_DB(otros_usuarios, "auth_user.username")
        ]
        res = db(db.auth_user.id == id).validate_and_update(**vars)
        if (res.errors):
            response.status = 422
            return response.json(res.errors)
        # Membership
        from applications.sms.modules.db.auth import update_membership
        
        update_membership(id, grupos)

        return response.json(res) 
            
    @auth.requires_membership('administrador')
    def DELETE(id):
        res = db(db.auth_user.id == id).delete()
        return response.json(res)
    
    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals() 
