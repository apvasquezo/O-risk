from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from infrastructure.database.db_config import Base, engine

# Importa todos los routers
from interfaces.controllers import (
    auth_controller,
    cause_controller,
    channel_controller,
    control_controller,
    consequence_controller,
    dashboard_controller,
    email_controller,
    evalControl_controller,
    eventLog_controller,
    event_controller,
    history_controller,
    impact_controller,
    macroprocess_controller,
    notification_controller,
    personal_controller,
    plan_controller,
    plancontrol_controller,
    process_controller,
    probability_controller,
    product_controller,
    profile_controller,
    recover_controller,
    riskcategory_controller,
    riskcontroltype_controller,
    riskfactor_controller,
    risktype_controller,
    role_controller,
    tracking_controller,
    user_controller,
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
        allow_origins=[
            "http://localhost:3000",
            "http://192.168.1.20:3000"],
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
        cause_controller.router,
        channel_controller.router,
        control_controller.router,
        consequence_controller.router,
        dashboard_controller.router,
        email_controller.router,
        evalControl_controller.router,
        eventLog_controller.router,
        event_controller.router,
        history_controller.router,
        impact_controller.router,
        macroprocess_controller.router,
        notification_controller.router,
        personal_controller.router,
        plan_controller.router,
        plancontrol_controller.router,
        process_controller.router,
        probability_controller.router,
        product_controller.router,
        profile_controller.router,
        recover_controller.router,
        riskcategory_controller.router,
        riskcontroltype_controller.router,
        riskfactor_controller.router,
        risktype_controller.router,
        role_controller.router,
        tracking_controller.router,
        user_controller.router,
    ]

    for router in routers:
        app.include_router(router)

    return app

app = create_app()
