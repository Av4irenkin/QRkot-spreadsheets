from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.constants import (
    MIN_LENGTH_NAME,
    MAX_LENGTH_NAME,
    MIN_LENGTH_DESCRIPTION
)


NAME_EXAMPLE = 'Помощь бездомным котикам'
DESCRIPTION_EXAMPLE = 'Сбор средств на лечение бездомных кошек'
FULL_AMOUNT_EXAMPLE = 1000
FULL_AMOUNT_UPDATE_EXAMPLE = 1


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=MIN_LENGTH_NAME,
        max_length=MAX_LENGTH_NAME,
        examples=[NAME_EXAMPLE]
    )
    description: str = Field(
        ...,
        min_length=MIN_LENGTH_DESCRIPTION,
        examples=[DESCRIPTION_EXAMPLE]
    )
    full_amount: int = Field(
        ...,
        gt=0,
        examples=[FULL_AMOUNT_EXAMPLE]
    )

    model_config = ConfigDict(
        extra='forbid'
    )


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH_NAME,
        max_length=MAX_LENGTH_NAME
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH_DESCRIPTION
    )
    full_amount: Optional[int] = Field(
        None,
        gt=0,
        examples=[FULL_AMOUNT_UPDATE_EXAMPLE]
    )

    model_config = ConfigDict(
        extra='forbid'
    )


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )
