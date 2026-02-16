from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router,
    donation_router,
    user_router,
    google_api_router
)
from app.constants import (
    CHARITY_PROJECT_ROUTER_PREFIX,
    CHARITY_PROJECT_ROUTER_TAG,
    DONATION_ROUTER_PREFIX,
    DONATION_ROUTER_TAG,
    GOOGLE_ROUTER_PREFIX,
    GOOGLE_ROUTER,
)


main_router = APIRouter()
main_router.include_router(
    charity_project_router,
    prefix=CHARITY_PROJECT_ROUTER_PREFIX,
    tags=[CHARITY_PROJECT_ROUTER_TAG]
)
main_router.include_router(
    donation_router,
    prefix=DONATION_ROUTER_PREFIX,
    tags=[DONATION_ROUTER_TAG]
)
main_router.include_router(user_router)
main_router.include_router(
    google_api_router,
    prefix=GOOGLE_ROUTER_PREFIX,
    tags=[GOOGLE_ROUTER]
)
