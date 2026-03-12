from sqlmodel import Session, select

class BaseService:
    def __init__(self, model: type, session: Session):
        self.model = model
        self.session = session


    def get_all(self, include_disabled: bool = False):
        stmt = select(self.model)
        if not include_disabled:
            stmt = stmt.where(self.model.disabled == False)
        return self.session.exec(stmt).all()


    def get_by_id(self, id: int):
        return self.session.get(self.model, id)
    

    def create(self, obj_in):
        obj = self.model.model_validate(obj_in)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
    

    def remove(self, id: int, soft: bool = True):
        obj = self.get_by_id(id)
        if obj:
            if soft:
                obj.disabled = True
                self.session.add(obj)
            else:
                self.session.delete(obj)
            self.session.commit()
            return True
        return False