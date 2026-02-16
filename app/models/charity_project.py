from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.constants import MAX_LENGTH_NAME
from app.models.investment import Investment


class CharityProject(Investment):

    name: Mapped[str] = mapped_column(
        String(MAX_LENGTH_NAME),
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    def __repr__(self) -> str:
        return '{}, name={}'.format(
            super().__repr__(),
            self.name
        )
