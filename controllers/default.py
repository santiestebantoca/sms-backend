# -*- coding: utf-8 -*-

from threading import Thread


def run_in_thread(fn):
    def run(*k, **kw):
        t = Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t

    return run


@run_in_thread
def send_email(email_list, subject, message):
    footer = "SupervisiÃ³n DTCA"
    mail.send(to=email_list, subject=subject, message=message + "\n\n" + footer)


use_smsgw = True  # False to use API in 10.30.12.8

if use_smsgw and request.function == "send":
    smsgw = DAL(app_config.get("db.smsgw"), migrate=False)
    smsgw.define_table("outbox", Field("number"), Field("text"), Field("sender"))


def index():
    return dict()


@request.restful()
def send():

    def POST(*args, **vars):
        """
        vars (texto, destinatarios)
        insert into db.mensaje and db.envio
        and then a callback on db.destinatario.insert makes the calls to SMS API
        """

        success = []
        mensaje_data = {
            "de": auth.user_id,
            "texto": vars["texto"],
            "continua": vars["continua"],
            "previo": vars["previo"],
        }
        # Update `subgrupo` if `previo` with `previo`.`subgrupo` or `previo`.`id`
        if vars["previo"]:
            previo = db.mensaje(vars["previo"])
            subgrupo = previo.subgrupo or previo.id
            mensaje_data.update(subgrupo=subgrupo)
        #
        api_data = {"text": vars["texto"], "sender": "AVISO DTCA"}
        mensaje = db.mensaje.validate_and_insert(**mensaje_data)
        if mensaje["id"]:
            envio_data = {"mensaje_id": mensaje["id"]}
            for suscriptor_id in vars["destinatarios"]:
                envio_data["suscriptor_id"] = suscriptor_id
                envio = db.envio.validate_and_insert(**envio_data)
                if envio["id"]:
                    suscriptor = db.suscriptor(suscriptor_id)
                    if suscriptor:
                        api_data["number"] = suscriptor.telefono
                        if use_smsgw:
                            if smsgw.outbox.insert(**api_data) == 1:
                                success.append(suscriptor.id)
                        else:
                            if send_api(api_data) == "1":
                                success.append(suscriptor.id)
                        if suscriptor.correo:
                            send_email(
                                [suscriptor.correo],
                                "Aviso de SupervisiÃ³n DTCA.",
                                api_data["text"],
                            )
        # Update previo `continua` = False
        if vars["previo"]:
            db(db.mensaje.id == vars["previo"]).update(continua=False)

        return response.json({"id": mensaje["id"], "errors": {}, "success": success})

    def OPTIONS(*args, **vars):
        raise HTTP(200, **headers)

    return locals()


def send_api(data):
    from urllib.request import urlopen
    from urllib.parse import urlencode

    url = app_config.get('api_sms.enviar')
    data_encode = urlencode(data).encode()  # to binary
    with urlopen(url, data_encode) as res:
        binary = res.read()
        return binary.decode()  # to str


def emailtest():
    return mail.send(
        # to=[auth.user.email],
        to=request.args(0),
        subject='Correo de prueba de SMS',
        message='Correo de prueba de SMS'
    )  # True or False
