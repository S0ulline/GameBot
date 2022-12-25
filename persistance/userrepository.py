from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeMeta
from persistance.sqlalchemy_orm import User, UserDiceInfo

T = TypeVar('T')


class Repository(Generic[T]):
    session: Session
    type: DeclarativeMeta

    def __init__(self, session: Session, entity_type: DeclarativeMeta):
        """ Констуктор """
        self.type = entity_type
        self.session = session

    def get(self, id) -> T:
        """ Получение """
        user_query = select(self.type).where(self.type.id == id)
        result = self.session.execute(user_query).fetchone()
        if result is None:
            return None
        entity_type_name = getattr(result, self.type.__name__)
        return entity_type_name

    def add(self, entity: T) -> None:
        """ Добавление """
        self.session.add(entity)


class UnitOfWork:
    user_repository: Repository[User]
    user_dice_info_repository: Repository[UserDiceInfo]
    _session: Session

    def __init__(self, engine: Engine):
        """ Констуктор """
        self._session = sessionmaker(engine)()
        self.user_repository = Repository[User](self._session, User)
        self.user_dice_info_repository = Repository[UserDiceInfo](self._session, UserDiceInfo)

    def save_changes(self):
        self._session.commit()
