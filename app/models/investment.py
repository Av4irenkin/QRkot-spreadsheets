from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Boolean, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Common


class Investment(Common):
    __abstract__ = True
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
        return ('{}, full_amount={}, invested_amount={}, fully_invested={}, '
                'create_date={}, close_date={}').format(
            super().__repr__(),
            self.full_amount,
            self.invested_amount,
            self.fully_invested,
            self.create_date,
            self.close_date
        )
