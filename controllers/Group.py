from fastapi import HTTPException,status
from models.Group import Group


class GroupService:
        
        def __init__(self, db_session):
            self.db_session = db_session

        def create_user(self, group_data):
                new_user = Group(
                    owner_id = group_data.email,
                    name = group_data.name
                )
                try:
                    self.db_session.add(new_user)
                    self.db_session.commit()
                    
                except Exception as e:
                    self.db_session.rollback()
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}")
                
                return self.db_session.query(Group).filter(Group.owner_id == group_data.email).all()[-1]
            
        # def get_users(self):
        #     try:
        #         user = self.db_session.query(User).all()
        #         return user
        #     except Exception as e:
        #         self.db_session.rollback()
        #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No existen usuarios")

        
        def get_grouo_id(self, group_id):
            try:
                user = self.db_session.query(Group).filter(Group.id == group_id).first()
                
                if not user:
                    raise HTTPException(status_code=404, detail="Group not found")
                return user
                
            except HTTPException as http_error:
                raise http_error

            except Exception as e:
                self.db_session.rollback()
                raise HTTPException(status_code=500, detail=f"An error occurred:  {str(e)}")