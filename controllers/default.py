# -*- coding: utf-8 -*-


def index():
    return dict()


def emailtest():
    return mail.send(
        to=request.args(0),
        subject='Correo de prueba de SMS',
        message='Correo de prueba de SMS'
    )  # True or False
