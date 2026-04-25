# -*- coding: utf-8 -*-

from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth, Service, PluginManager
from gluon.contrib.login_methods.ldap_auth import ldap_auth

request.requires_https()

app_config = AppConfig(reload=False)

db = DAL(
    app_config.get("db.sms"),
    pool_size=10,
    check_reserved=["all"],
    migrate=False,
    migrate_enabled=False
)

session.connect(request, response, db, masterapp=None)

auth = Auth(db)
service = Service()
plugins = PluginManager()

# extra fields
auth.settings.extra_fields["auth_user"] = [auth.signature]
auth.define_tables(username=True)

# configure email
mail = auth.settings.mailer
mail.settings.server = app_config.get("smtp.server")
mail.settings.sender = app_config.get("smtp.sender")
mail.settings.login = app_config.get("smtp.login")
mail.settings.tls = app_config.get("smtp.tls") or False
mail.settings.ssl = app_config.get("smtp.ssl") or False

# configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.remember_me_form = False
auth.settings.create_user_groups = False
auth.settings.actions_disabled = [
    "register",
    "change_password",
    "request_reset_password",
    "retrieve_username",
    "profile",
]
auth.settings.expiration = 86400  # 24 hora (por defecto 3600: 1 hora)

# ds.etecsa.cu
# auth.settings.login_methods.append(
#     ldap_auth(
#         server='192.168.91.114',
#         base_dn='ou=etecsa.cu,ou=People,dc=etecsa,dc=cu')
# )

# lds.etecsa.cu
auth.settings.login_methods.append(
    ldap_auth(
        server='172.29.30.200',
        base_dn='ou=etecsa.cu,ou=People,dc=etecsa,dc=cu',
        secure=True,
        self_signed_certificate=True,
        # tls=True,
        logging_level='debug')
)

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

tabla = db.define_table

T.force("es")

"""
As long as possible, we use validate_and_update/insert rather than update or SQLFORM
* validate_and_update returns an Object with 'updated' and 'errors' which is a standard on client side
* validate_and_insert returns an Object with 'id' and 'errors' which is a standard on client side
"""

# CORS Policy (RESTFUL API )
"""
Using X-Requested-With header, implies using OPTIONS for any method (GET, POST, ...)
We force X-Requested-With: XMLHttpRequest in client request,
that is the way web2py recognizes the ajax request.
"""

# frontURL = myconf.get('front.url', request.env.http_origin)
frontURL = request.env.http_origin

response.headers["Access-Control-Allow-Origin"] = frontURL
response.headers["Access-Control-Allow-Credentials"] = "true"

headers = {
    "Access-Control-Allow-Origin": frontURL,
    "Access-Control-Allow-Credentials": "true",
    "Access-Control-Allow-Headers": "X-Requested-With, Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT",
    # 24hrs  // cache for Allow Header & Allow Methods
    "Access-Control-Max-Age": 86400,
}

# response.headers.update(**headers)

if request.ajax:

    def resp401():
        raise HTTP(401, **headers)


    def resp403():
        raise HTTP(403, **headers)

    auth.settings.on_failed_authentication = resp401
    auth.settings.on_failed_authorization = resp403
