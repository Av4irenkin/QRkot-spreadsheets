from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    declared_attr
)

from app.core.db import Base


class Common(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    def __repr__(self) -> str:
        return f'{type(self).__name__} id={self.id}'
