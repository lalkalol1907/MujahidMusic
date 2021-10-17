from peewee import *
from config import DBCFG

cfg = DBCFG()

DataBaseHandler = MySQLDatabase(database=cfg.DB, 
                                user=cfg.USERNAME, password=cfg.PASSWORD, 
                                host=cfg.HOST, charset=cfg.CHARSET)

class BaseModel(Model):
    class Meta:
        database = DataBaseHandler

class User(BaseModel):
    id = PrimaryKeyField(null=False)
    tg_user_id = CharField()
    ds_user_id = CharField()
    servers = TextField()
    server_id = TextField()
    class Meta:
        db_table = "users"

class Server(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField()
    server_id = TextField()
    reg_key = IntegerField()
    class Meta:
        db_table = "servers"