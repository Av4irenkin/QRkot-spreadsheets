from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User


class CRUDDonation(CRUDBase[Donation]):

    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> list[Donation]:
        return (await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            ).order_by(Donation.create_date.desc())
        )).scalars().all()


donation_crud = CRUDDonation(Donation)
