from sqlalchemy.orm import class_mapper
from fastapi import status
from fastapi import HTTPException
from config.db import session

def add_to_db(item):
    try:
        session.add(item)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_to_db(item):
    try:
        session.delete(item)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def check_column(column,model):
    if column not in model.__table__.columns:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid column name: {column}")



def instance_to_dict(instance):

    """Convierte una instancia de un modelo SQLAlchemy en un diccionario."""
    return {column.key: getattr(instance, column.key)
            for column in class_mapper(instance.__class__).columns}