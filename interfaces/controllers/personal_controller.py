from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database.db_config import get_db
from domain.repositories.personal_repository import PersonalRepository
from application.use_case.manage_personal import (
    create_personal,
    get_personal,
    get_all_personal,
    update_personal,
    delete_personal
)

router = APIRouter()

# Schemas para las solicitudes y respuestas
class PersonalCreate(BaseModel):
    id_personal: str
    name: str
    position: str
    area: Optional[str]
    email: Optional[str]

class PersonalResponse(BaseModel):
    id_personal: str
    name: str
    position: str
    area: Optional[str]
    email: Optional[str]

@router.post("/personal/", response_model=PersonalResponse)
async def create_personal_endpoint(personal: PersonalCreate, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    created_personal = await create_personal(personal, repository)
    return PersonalResponse(
        id_personal=created_personal.id_personal,
        name=created_personal.name,
        position=created_personal.position,
        area=created_personal.area,
        email=created_personal.email
    )

@router.get("/personal/{personal_id}", response_model=PersonalResponse)
async def read_personal(personal_id: str, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    personal = await get_personal(personal_id, repository)
    if personal is None:
        raise HTTPException(status_code=404, detail="Personal not found")
    return PersonalResponse(
        id_personal=personal.id_personal,
        name=personal.name,
        position=personal.position,
        area=personal.area,
        email=personal.email
    )

@router.get("/personal/", response_model=List[PersonalResponse])
async def read_all_personal(db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    personals = await get_all_personal(repository)
    return [
        PersonalResponse(
            id_personal=personal.id_personal,
            name=personal.name,
            position=personal.position,
            area=personal.area,
            email=personal.email
        ) for personal in personals
    ]

@router.put("/personal/{personal_id}", response_model=PersonalResponse)
async def update_personal(personal_id: str, personal: PersonalCreate, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    updated_personal = await update_personal(personal_id, personal, repository)
    if updated_personal is None:
        raise HTTPException(status_code=404, detail="Personal not found")
    return PersonalResponse(
        id_personal=updated_personal.id_personal,
        name=updated_personal.name,
        position=updated_personal.position,
        area=updated_personal.area,
        email=updated_personal.email
    )

@router.delete("/personal/{personal_id}", response_model=dict)
async def delete_personal(personal_id: str, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    try:
        await delete_personal(personal_id, repository)
        return {"detail": "Personal record deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))