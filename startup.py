import os

from sqlalchemy import create_engine

from payload import Payload
from persistance.sqlalchemy_orm import Base
from persistance.userrepository import UnitOfWork

if "Environment" in os.environ and os.environ["Environment"] == "Production":
    with open("config.json") as config:
        data = config.read()
else:
    with open("config.development.json") as config:
        data = config.read()

p = Payload(data)
bot_api = p.BOT_API_TOKEN
postgre_conn = p.POSTGRESQL_CONNECT

engine = create_engine(postgre_conn)
Base.metadata.create_all(engine)

db = UnitOfWork(engine=engine)
