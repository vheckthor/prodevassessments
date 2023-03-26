from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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

    # quest_scheduler_app.include_router(appointments_router)
    # quest_scheduler_app.include_router(psc_router)
    return assessments_app


app = pro_dev_assessments()
