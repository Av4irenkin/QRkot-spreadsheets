from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.constants import MIN_DONATION_AMOUNT


COMMENT_EXAMPLE = 'На корм котикам'


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0, examples=[MIN_DONATION_AMOUNT])
    comment: Optional[str] = Field(None, examples=[COMMENT_EXAMPLE])
    model_config = ConfigDict(
        extra='forbid'
    )


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    comment: Optional[str]
    full_amount: int
    create_date: datetime
    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )


class DonationFullInfoDB(DonationDB):
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: Optional[int]
    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )
