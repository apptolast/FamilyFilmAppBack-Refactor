from fastapi import HTTPException,status
from controllers.MovieGroupUser import MovieUserGroupService
from models.Group import Group

class GroupService:
        
        def __init__(self, db_session):
            self.db_session = db_session

        def create_group(self, name, ownerID):
            new_group = Group(
                 name = name,
                 owner_id = ownerID
            )
            try:
                self.db_session.add(new_group)
                self.db_session.commit()
                grupo = self.db_session.query(Group).filter(Group.owner_id == ownerID).all()[-1]
                MovieUserGroupService.create_union_user(user_id=ownerID,group_id=grupo.id)
            except Exception as e:
                 self.db_session.rollback()
                 raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
            
            return grupo
        
        def get_groups(self,user_id):
            return MovieUserGroupService.get_groups(user_id=user_id)
            
        
        def get_group_id(self, gruop_id):
            return MovieUserGroupService.get_group_id(gruop_id=gruop_id)

