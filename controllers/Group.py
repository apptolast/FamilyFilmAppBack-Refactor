from fastapi import HTTPException,status
from sqlalchemy import and_
from controllers.MovieGroupUser import MovieUserGroupService
from models.Group import Group
from models.MovieUserGroup import MovieUserGroup

class GroupService:
        
        def __init__(self, db_session,movie_user_group_repository):
            self.movie_user_group_repository = movie_user_group_repository
            self.db_session = db_session

        def create_group(self, name, ownerID):
            new_group = Group(
                 name = name,
                 owner_id = ownerID
            )
            try:
                self.db_session.add(new_group)
                self.db_session.commit()
                group = self.db_session.query(Group).filter(Group.owner_id == ownerID).all()[-1]
                self.movie_user_group_repository.create_union_user(user_id=ownerID,group_id=group.id)
            except Exception as e:
                 self.db_session.rollback()
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
            
            return group
        
        def get_groups(self,user_id):
            return self.movie_user_group_repository.get_groups(user_id=user_id)
            
        def get_group_id(self, gruop_id):
            return self.movie_user_group_repository.get_group_id(gruop_id=gruop_id)

        def add_user_to_group(self,user_id,group_id,owner_id):
            try:
                if self.is_owner(owner_id,group_id) is None:
                    raise HTTPException(status_code=404, detail="User not Owner")

                self.movie_user_group_repository.create_union_user(user_id,group_id)    
                return self.db_session.query(MovieUserGroup).filter(MovieUserGroup.id_group == group_id).all()

            except HTTPException as http_error:
                raise http_error
            
        def delete_user_to_group(self,user_id,group_id,owner_id):
            try:
                if self.is_owner(owner_id,group_id) is None:
                    raise HTTPException(status_code=404, detail="User not Owner")
                self.movie_user_group_repository.delete_union_user(user_id,group_id)    
                return self.db_session.query(MovieUserGroup).filter(MovieUserGroup.id_group == group_id).first()

            except HTTPException as http_error:
                raise http_error

        def delete_user_and_group(self,users_id,group_id,owner_id):
            for user_id in users_id:
                self.delete_user_to_group(user_id.id,group_id,owner_id)

        def is_owner(self,user_id,group_id):
            try:
                group = self.db_session.query(Group).filter(and_(Group.owner_id == user_id, Group.id == group_id)).first()
                return group
            except Exception as e:
                 self.db_session.rollback()
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"User is not owner")
           
        def add_to_watch(self,user_id,group_id,movie_id):
            self.movie_user_group_repository.create_union_group_movie(group_id,movie_id,user_id,False)

        def delete_to_watch(self,user_id,group_id,movie_id):
            self.movie_user_group_repository.delete_union_group_movie(group_id,movie_id,user_id,False)
        
        def add_to_watched(self,user_id,group_id,movie_id):
            self.movie_user_group_repository.create_union_group_movie(group_id,movie_id,user_id,True)

        def delete_to_watched(self,user_id,group_id,movie_id):
            self.movie_user_group_repository.delete_union_group_movie(group_id,movie_id,user_id,True)
        