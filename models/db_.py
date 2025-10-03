# -*- coding: utf-8 -*-
__author__ = "jorge.santiesteban"


# tabla('territorio',
#       Field('nombre', notnull=True),
#       Field('orden', 'integer'),
#       format=' %(nombre)s')

tabla(
    "grupo",
    Field("nombre", notnull=True),
    Field("apodo"),
    # Field('territorio_id', 'reference territorio', notnull=True),
    Field("pertenece", "reference grupo"),
    Field("descripcion"),
    Field("label"),
)

tabla(
    "suscriptor",
    Field("nombre", notnull=True),
    Field("cargo"),
    Field("telefono", "integer", notnull=True, unique=True),
    Field("grupo", "reference grupo"),
    Field("activo", "boolean", default=True),
    Field("suplente", "reference suscriptor"),
    Field("correo", requires=IS_EMPTY_OR(IS_EMAIL())),
    auth.signature,
)

tabla(
    "notifica", Field("grupo_a", "reference grupo"), Field("grupo_b", "reference grupo")
)

tabla(
    "mensaje",
    Field("de", "reference auth_user"),
    Field("en", "datetime", default=request.now),
    Field("texto"),
    Field("continua", "boolean"),
    Field("previo", "reference mensaje"),
    Field("subgrupo", "reference mensaje"),
)

tabla(
    "envio",
    Field("mensaje_id", "reference mensaje"),
    Field("suscriptor_id", "reference suscriptor"),
    Field("enviado", "boolean"),
)

tabla("plantilla", Field("texto"), auth.signature)
## Rules

db.grupo.apodo.requires = [
    IS_EMPTY_OR(IS_NOT_IN_DB(db, "grupo.apodo", error_message="Ya existe el alias"))
]
