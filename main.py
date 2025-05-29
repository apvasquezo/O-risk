from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from infrastructure.database.db_config import Base, engine
from routers import recover


# Importa todos los routers
from interfaces.controllers import (
    auth_controller,
    user_controller,
    role_controller,
    riskcategory_controller,
    risktype_controller,
    riskfactor_controller,
    riskcontroltype_controller,
    control_controller,
    event_controller,
    probability_controller,
    cause_controller,
    consequence_controller,
    impact_controller,
    tracking_controller,
    process_controller,
    macroprocess_controller,
    plan_controller,
    personal_controller,
    channel_controller,
    product_controller,
    notification_controller,
    history_controller,
    eventLog_controller,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Configuración de CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {"message": "Gestionando Riesgos"}

    # Lista de routers
    routers = [
        auth_controller.router,
        user_controller.router,
        role_controller.router,
        riskcategory_controller.router,
        risktype_controller.router,
        riskfactor_controller.router,
        riskcontroltype_controller.router,
        control_controller.router,
        event_controller.router,
        probability_controller.router,
        cause_controller.router,
        consequence_controller.router,
        impact_controller.router,
        tracking_controller.router,
        process_controller.router,
        macroprocess_controller.router,
        plan_controller.router,
        personal_controller.router,
        channel_controller.router,
        product_controller.router,
        notification_controller.router,
        history_controller.router,
        eventLog_controller.router,
        recover.router,
    ]

    for router in routers:
        app.include_router(router)

    return app

app = create_app()
