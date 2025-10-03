# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


tabla(
    "vw_notifica",
    Field("grupo_a", "reference grupo"),
    Field("grupo_b", "reference grupo"),
    Field("nombre", notnull=True),
    migrate=False,
)

tabla(
    "vw_envio",
    Field("mensaje_id", "reference mensaje"),
    Field("suscriptor_id", "reference suscriptor"),
    Field("enviado", "boolean"),
    Field("suscriptor"),
    Field("grupo_id"),
    Field("grupo"),
    migrate=False,
)

tabla("vw_plantilla", Field("texto"), Field("modified_by"))

tabla("usuario", Field("name"), Field("username"))

tabla("vw_mensaje",
    Field("de"),
    Field("en", "datetime"),
    Field("texto"),
    Field("continua", "boolean"),
    Field("previo", "reference mensaje"),
    Field("subgrupo", "reference mensaje"),
    Field("de_id", "reference auth_user"),
    migrate=False,
)
