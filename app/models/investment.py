from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Boolean, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from app.core.db import Base


class Investment(Base):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='check_full_amount_positive'
        ),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_range'
        ),
    )

    def __init__(self, **kwargs):
        kwargs.setdefault('invested_amount', 0)
        super().__init__(**kwargs)

    def close_if_fully_invested(self):
        if self.invested_amount >= self.full_amount:
            self.fully_invested = True
            self.close_date = datetime.now()

    def __repr__(self) -> str:
        return ('{} id={}, full_amount={}, invested_amount={}, '
                'fully_invested={}, create_date={}, close_date={}').format(
            self.__class__.__name__,
            self.id,
            self.full_amount,
            self.invested_amount,
            self.fully_invested,
            self.create_date,
            self.close_date
        )
