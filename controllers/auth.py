# -*- coding: utf-8 -*-
__author__ = 'jorge.santiesteban'


@request.restful()
def login():
    def GET():
        return response.json(user())

    def POST(**vars):
        login_bare(vars['username'], vars['password'])
        return response.json(user())

    def DELETE():
        if auth.user:
            log = auth.messages['logout_log']
            auth.log_event(log, auth.user, origin='auth')
            auth.logout_bare()
        return response.json(user())

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


def user():
    if auth.user:
        return dict(
            id=auth.user_id,
            name='{first_name} {last_name}'.format(**auth.user).strip(),
            username=auth.user.username,
            admin=auth.has_membership('administrador'),
            is_impersonating=auth.is_impersonating(),
            can_impersonate=can_impersonate(),
        )
    return auth.user


def login_bare(username, password):
    """
    A version of Auth.login_bare from gluon.tools customized for this app
    In this version, user must be in database to login
    Differences:
    No auth login method / No password validation for local request
    """
    def let(user):
        auth.login_user(user)
        auth.log_event(auth.messages['login_log'], user)
        return user

    user = db.auth_user(username=username)
    if user:
        if request.is_local:
            return let(user)
        for login_method in auth.settings.login_methods:
            if login_method != auth and login_method(username, password):
                if (user.registration_key is None
                        or not user.registration_key.strip()):
                    return let(user)
    message = 'Login failed with credentials %(username)s; %(password)s'
    args = dict(username=username, password=password)
    auth.log_event(message % args)
    return False


@request.restful()
def impersonate():
    def POST(*args, **vars):
        if can_impersonate():
            auth.impersonate(request.args(0) or '0')
        else:
            auth.impersonate('0')
        return response.json(user())

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


@request.restful()
def users():
    def GET(*args, **vars):
        if 'name' in vars:
            q = db.usuario.name.contains(vars['name'])
            res = db(q).select(limitby=(0, 10))
        else:
            res = db(db.usuario).select()
        return response.json(res)

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


def can_impersonate():
    return auth.user_id in [1, 2, 3]
