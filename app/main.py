from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.api_v1.endpoints.user import user_router
from app.api.api_v1.endpoints.accounts import account_router

from app.config import settings

def pro_dev_assessments() -> FastAPI:
    """
    Returns a FastAPI app object.
    """

    assessments_app = FastAPI(
        title=settings.Settings().PROJECT_NAME,
        openapi_url=f"{settings.Settings().API_V1_STR}/openapi.json",
        version="0.1.0",
    )

    if settings.Settings().BACKEND_CORS_ORIGINS:
        assessments_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    assessments_app.include_router(user_router)
    assessments_app.include_router(account_router)
    return assessments_app


app = pro_dev_assessments()
