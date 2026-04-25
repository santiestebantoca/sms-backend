# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"
from gluon.contrib.appconfig import AppConfig
from threading import Thread

app_config = AppConfig(reload=False)

use_smsgw = app_config.get('sms.use_smsgw', default=True)
sms_sender = app_config.get('sms.sender', default='AVISO DTCA')
email_subject = app_config.get('sms.email_subject', default='Aviso de Supervisión DTCA.')
email_footer = app_config.get('sms.email_footer', default='Supervisión DTCA')


def run_in_thread(fn):
    def wrapper(*args, **kwargs):
        t = Thread(target=fn, args=args, kwargs=kwargs)
        t.start()
        return t
    return wrapper


def send_api(data):
    from urllib.request import urlopen
    from urllib.parse import urlencode
    url = app_config.get('api_sms.enviar')
    data_encode = urlencode(data).encode()  # to binary
    with urlopen(url, data_encode) as res:
        binary = res.read()
        return binary.decode()  # to str


@run_in_thread
def send_email_task(email_list, subject, message, mail_obj):
    mail_obj.send(to=email_list, subject=subject,
                  message=message + "\n\n" + email_footer)


def notificar(suscriptor, texto, db_smsgw=None, mail_obj=None):
    api_data = {
        "number": suscriptor.telefono,
        "text": texto,
        "sender": sms_sender
    }

    if use_smsgw and db_smsgw is not None:
        db_smsgw.outbox.insert(**api_data)
    elif not use_smsgw:
        send_api(api_data)

    if suscriptor.correo and mail_obj is not None:
        send_email_task(
            [suscriptor.correo],
            email_subject,
            api_data["text"],
            mail_obj)
