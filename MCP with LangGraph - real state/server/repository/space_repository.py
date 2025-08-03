from sqlalchemy.orm import Session
from model.space import Space
from config.database_config import get_session

class SpaceRepository:
    def __init__(self, session: Session = get_session()):
        self.db: Session = session


    def get_by_id(self, space_id: int):
        return self.db.query(Space).filter(Space.id == space_id).first()


    def get_all(self):
        return self.db.query(Space).all()


    def create(self, space: Space):
        self.db.add(space)
        self.db.commit()
        self.db.refresh(space)
        return space


    def update(self, space_id: int, **kwargs):
        space = self.get_by_id(space_id)
        if not space:
            return None
        for key, value in kwargs.items():
            if hasattr(space, key):
                setattr(space, key, value)
        self.db.commit()
        self.db.refresh(space)
        return space


    def delete(self, space_id: int):
        space = self.get_by_id(space_id)
        if not space:
            return False
        self.db.delete(space)
        self.db.commit()
        return True


    def close(self):
        self.db.close()
