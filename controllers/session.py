
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

        