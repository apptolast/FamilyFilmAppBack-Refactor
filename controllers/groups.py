from config.db import session
from controllers.session import instance_to_dict
from models import Genre, GroupUser, Movie
from models.Group import Group as GroupModel
from schema import Group as GroupSchema
from schema.Movie import ShowMovie, movieData
from models.WatchList import WatchList
from models.ViewList import ViewList

def get_group_by_id(id:int):
    return session.query(GroupModel).filter(GroupModel.id == id).first()

def get_group_all():
    return session.query(GroupModel).all()

def get_genre_names(genre_ids, idiom):
    return [session.query(Genre.name).filter(Genre.id == genre_id).first()[0][idiom] for genre_id in genre_ids]

def GroupData_id(id:int,idiom:str):
    group = get_group_by_id(id)
    
    user_owner = session.query(GroupUser).filter((GroupUser.group_id == group.id)).first().user_id
    
    users = [group_user.user for group_user in session.query(GroupUser).filter((GroupUser.group_id == group.id)).all()]

    wls_db_data = session.query(WatchList).filter(WatchList.group_id == group.id).all()
    vls_db_data = session.query(ViewList).filter(ViewList.group_id == group.id).all()

    wls = [movieData(group_id= group.id, movie_id=wl.movie_id, movie=ShowMovie(
        id=wl.movie.id,
        adult=wl.movie.adult,
        title=wl.movie.title[idiom],
        genres = get_genre_names(wl.movie.genre_ids, idiom),
        language=wl.movie.language,
        synopsis=wl.movie.synopsis[idiom],
        image=wl.movie.image,
        release_date=wl.movie.release_date,
        vote_average=wl.movie.vote_average,
        vote_count=wl.movie.vote_count
    )) for wl in wls_db_data] if wls_db_data else []
    
    vls = [movieData(group_id= group.id, movie_id=vl.movie_id, movie=ShowMovie(
        id=vl.movie.id,
        title=vl.movie.title[idiom],
        synopsis=vl.movie.synopsis[idiom],
        genres = get_genre_names(vl.movie.genre_ids, idiom),
        language=vl.movie.language,
        image=vl.movie.image,
        release_date=vl.movie.release_date,
        vote_average=vl.movie.vote_average,
        vote_count=vl.movie.vote_count
    )) for vl in vls_db_data] if vls_db_data else []    
    
    return GroupSchema.GroupData(
        id=group.id, 
        name=group.name,  
        user_owner_id=user_owner,
        watchlist=wls,
        viewlist=vls,
        users=[{"userId": user.id, "email": user.email, "firebaseUuid": "", "role": user.role} for user in users]
    )

def GroupData_all(idiom):
    groups = get_group_all()
    return [GroupData_id(group.id,idiom) for group in groups]