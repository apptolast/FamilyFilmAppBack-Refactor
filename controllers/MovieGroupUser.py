from fastapi import HTTPException,status
from sqlalchemy import and_, distinct
from models.MovieUserGroup import MovieUserGroup
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class MovieUserGroupService:
        
        def __init__(self, db_session):
            self.db_session = db_session


        def create_union_user(self,user_id, group_id,):
            new_group_asotiation = MovieUserGroup(
                id_movie = 0,
                id_user = user_id,
                id_group= group_id,
                toWatch = False,
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
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")
            
        def get_group_id(self,gruop_id):
            try:
                group = self.db_session.query(MovieUserGroup).filter(MovieUserGroup.id_group == gruop_id).all()
                
                if not group:
                    raise HTTPException(status_code=404, detail="Group not found")
                return group
                
            except HTTPException as http_error:
                raise http_error

            except Exception as e:
                self.db_session.rollback()
                raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")

        def delete_union_user(self, user_id, group_id):
            try:
                # Eliminar todas las asociaciones de películas para el usuario en el grupo
                deleted_count = self.db_session.query(MovieUserGroup).filter(
                    and_(
                        MovieUserGroup.id_group == group_id,
                        MovieUserGroup.id_user == user_id
                    )
                ).delete(synchronize_session=False)
                
                if deleted_count == 0:
                    raise HTTPException(status_code=404, detail="User not found in the group")

                # Commit the transaction if records were deleted
                self.db_session.commit()

            except SQLAlchemyError as e:
                # Revertir cambios en caso de error
                self.db_session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

            except Exception as e:
                # Captura de errores generales
                self.db_session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {e}")

        def create_union_group_movie(self,group_id,movie_id,user_id,is_to_Watch):
            new_group_asotiation = MovieUserGroup(
                id_movie= movie_id,
                id_user = user_id,
                id_group= group_id,
                toWatch = is_to_Watch
            )
            try:
                self.db_session.add(new_group_asotiation)
                self.db_session.commit()
            except Exception as e:
                 self.db_session.rollback()
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")

        def delete_union_group_movie(self,group_id,movie_id,user_id,is_to_Watch):
            try:
                delete = self.db_session.query(MovieUserGroup).filter(and_(MovieUserGroup.id_group == group_id, MovieUserGroup.id_movie == movie_id, MovieUserGroup.toWatch == is_to_Watch, MovieUserGroup.id_user == user_id)).first()
                
                if delete is None:
                    raise HTTPException(status_code=404, detail="Movie not is possible delete")

                self.db_session.delete(delete)
                self.db_session.commit()
            except Exception as e:
                 self.db_session.rollback()
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
        
            