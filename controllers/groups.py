from config.db import session
from controllers.movies import get_movie_by_id
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

def GroupData_id(id:int,idiom):
    group = get_group_by_id(id)

    user_owner = session.query(GroupUser).filter((GroupUser.group_id == group.id)).first().user_id
    
    users = [group_user.user for group_user in session.query(GroupUser).filter((GroupUser.group_id == group.id)).all()]

    wls_db_data = session.query(WatchList).filter(WatchList.group_id == group.id).all()
    vls_db_data = session.query(ViewList).filter(ViewList.group_id == group.id).all()

    wls = []
    if len(wls_db_data) >= 0:
        for wl in wls_db_data:
            movie_data = get_movie_by_id(wl.movie_id,idiom)

            if isinstance(movie_data,str):
                continue
        
            movieData(group_id= group.id, movie_id=int(id), movie=ShowMovie(
            id=movie_data.id,
            adult=movie_data.adult,
            title=movie_data.title,
            genres = get_genre_names(movie_data.genre_ids, idiom),
            language=movie_data.language,
            synopsis=movie_data.synopsis,
            image=movie_data.image,
            release_date=movie_data.release_date,
            vote_average=movie_data.vote_average,
            vote_count=movie_data.vote_count
            ))

    vls = []
    if len(vls_db_data) >= 0:
        for vl in vls_db_data:
            movie_data = get_movie_by_id(vl.movie_id,idiom)

            if isinstance(movie_data,str):
                continue
        
            movieData(group_id= group.id, movie_id=int(id), movie=ShowMovie(
            id=movie_data.id,
            adult=movie_data.adult,
            title=movie_data.title,
            genres = get_genre_names(movie_data.genre_ids, idiom),
            language=movie_data.language,
            synopsis=movie_data.synopsis,
            image=movie_data.image,
            release_date=movie_data.release_date,
            vote_average=movie_data.vote_average,
            vote_count=movie_data.vote_count
            ))    
    
    return GroupSchema.GroupData(
        id=group.id, 
        name=group.name,  
        user_owner_id=user_owner,
        watchlist=wls,
        viewlist=vls,
        users=[{"userId": user.id, "email": user.email, "firebaseUuid": "", "role": user.role} for user in users]
    )



def GroupData_all(me,idiom = 'en'):
    groups = get_group_all()
    groups_have = []
    
    for group in groups:
        group = GroupData_id(group.id,idiom)
        if group.users.__contains__(me.id):
            groups_have.append(group)
    