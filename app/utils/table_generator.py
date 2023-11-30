from sqlalchemy import Engine
from sqlalchemy.orm import DeclarativeMeta


def create_tables(base: DeclarativeMeta, engine: Engine, models: list[DeclarativeMeta]) -> None:
    tables = []
    for model in models:
        tables.append(model.__table__)

    base.metadata.create_all(bind=engine, tables=tables, checkfirst=True)
