from fastapi import HTTPException,status
from models.MovieUserGroup import MovieUserGroup
from schema.MovieUserGroup import MovieUserGroup 

class MovieUserGroupService:
        
        def __init__(self, db_session):
            self.db_session = db_session


        def create_union_user(self,user_id, group_id):
            new_group_asotiation = MovieUserGroup(
                id_movie = None,
                user_id = user_id,
                group_id = group_id,
                toWatch = None
            )
            try:
                self.db_session.add(new_group_asotiation)
                self.db_session.commit()
                
            except Exception as e:
                 self.db_session.rollback()
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")

        def get_groups(self,user_id):
            try:
                groups = self.db_session.query(MovieUserGroup).filter(MovieUserGroup.id_user == user_id).all()
                return groups
            except Exception as e:
                self.db_session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No existen usuarios {str(e)}")
            
        def get_group_id(self,gruop_id):
            try:
                gruop = self.db_session.query(MovieUserGroup).filter(MovieUserGroup.id_group == gruop_id).first()
                
                if not gruop:
                    raise HTTPException(status_code=404, detail="Gruop not found")
                return gruop
                
            except HTTPException as http_error:
                raise http_error

            except Exception as e:
                self.db_session.rollback()
                raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")

              