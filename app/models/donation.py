from typing import Optional

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.investment import Investment
from app.models.user import User


class Donation(Investment):

    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', name='fk_donation_user_id_user'),
        nullable=True
    )
    user: Mapped[User] = relationship(User)

    def __repr__(self) -> str:
        return '{}, comment={}, user_id={}'.format(
            super().__repr__(),
            self.comment,
            self.user_id
        )
