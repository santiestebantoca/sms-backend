# models/db_smsgw.py
from gluon.contrib.appconfig import AppConfig
from gluon import current

app_config = AppConfig(reload=False)

use_smsgw = app_config.get('sms.use_smsgw', default=True)

if use_smsgw:
    db_smsgw = DAL(app_config.get("db.smsgw"), migrate=False, pool_size=5)
    db_smsgw.define_table("outbox",
        db_smsgw.Field("number", length=20),
        db_smsgw.Field("text", "string", length=3000),
        db_smsgw.Field("sender")
    )
    current.db_smsgw = db_smsgw
else:
    db_smsgw = None
