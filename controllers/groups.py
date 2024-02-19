from config.db import session
from models import GroupUser
from models.Group import Group as GroupModel
from schema import Group as GroupSchema
from schema.Movie import ShowMovie, movieData
from models.WatchList import WatchList
from models.ViewList import ViewList

def get_group_by_id(id:int):
    return session.query(GroupModel).filter(GroupModel.id == id).first()

def get_group_all():
    return session.query(GroupModel).all()

def GroupData_id(id:int):
    group = get_group_by_id(id)
    
    user_owner = session.query(GroupUser).filter((GroupUser.group_id == group.id)).first().user_id
    
    users = [group_user.user for group_user in session.query(GroupUser).filter((GroupUser.group_id == group.id)).all()]

    wls_db_data = session.query(WatchList).filter(WatchList.group_id == group.id).all()
    vls_db_data = session.query(ViewList).filter(ViewList.group_id == group.id).all()

    wls = [movieData(group_id= group.id, movie_id=wl.movie_id, movie=ShowMovie(**wl.movie)) for wl in wls_db_data] if wls_db_data else []
    vls = [movieData(group_id= group.id, movie_id=vl.movie_id, movie=ShowMovie(**vl.movie)) for vl in vls_db_data] if vls_db_data else []

    return GroupSchema.GroupData(
        id=group.id, 
        name=group.name,  
        user_owner_id=user_owner,
        watchlist=wls,
        viewlist=vls,
        users=[{"userId": user.id, "email": user.email, "firebaseUuid": "", "role": user.role} for user in users]
    )

def GroupData_all():
    groups = get_group_all()
    return [GroupData_id(group.id) for group in groups]