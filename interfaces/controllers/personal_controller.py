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
    id: int
    name: str
    position: str
    area: Optional[str]
    process_id: Optional[int]
    email: Optional[str]

class PersonalResponse(BaseModel):
    id: int
    name: str
    position: str
    area: Optional[str]
    process_id: Optional[int]
    email: Optional[str]

@router.post("/personal/", response_model=PersonalResponse)
async def create_personal(personal: PersonalCreate, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    created_personal = await repository.create_personal(personal)
    return PersonalResponse(
        id=created_personal.id,
        name=created_personal.name,
        position=created_personal.position,
        area=created_personal.area,
        process_id=created_personal.process_id,
        email=created_personal.email
    )

@router.get("/personal/{personal_id}", response_model=PersonalResponse)
async def read_personal(personal_id: int, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    personal = await repository.get_personal(personal_id)
    if personal is None:
        raise HTTPException(status_code=404, detail="Personal not found")
    return PersonalResponse(
        id=personal.id,
        name=personal.name,
        position=personal.position,
        area=personal.area,
        process_id=personal.process_id,
        email=personal.email
    )

@router.get("/personal/", response_model=List[PersonalResponse])
async def read_all_personal(db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    personals = await repository.get_all_personal()
    return [
        PersonalResponse(
            id=personal.id,
            name=personal.name,
            position=personal.position,
            area=personal.area,
            process_id=personal.process_id,
            email=personal.email
        ) for personal in personals
    ]

@router.put("/personal/{personal_id}", response_model=PersonalResponse)
async def update_personal(personal_id: int, personal: PersonalCreate, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    updated_personal = await repository.update_personal(personal_id, personal)
    if updated_personal is None:
        raise HTTPException(status_code=404, detail="Personal not found")
    return PersonalResponse(
        id=updated_personal.id,
        name=updated_personal.name,
        position=updated_personal.position,
        area=updated_personal.area,
        process_id=updated_personal.process_id,
        email=updated_personal.email
    )

@router.delete("/personal/{personal_id}", response_model=dict)
async def delete_personal(personal_id: int, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    try:
        await repository.delete_personal(personal_id)
        return {"detail": "Personal record deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))