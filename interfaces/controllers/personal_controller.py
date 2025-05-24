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
from utils.auth import role_required

router = APIRouter(
    prefix="/personal",
    tags=["Personal"],
    dependencies=[Depends(role_required("super"))]
)

class PersonalCreate(BaseModel):
    id_personal: str
    name: str
    position: str
    area: Optional[str] = None
    email: Optional[str] = None

class PersonalResponse(BaseModel):
    id_personal: str
    name: str
    position: str
    area: Optional[str] = None
    email: Optional[str] = None


@router.post("/", response_model=PersonalResponse)
async def create_personal_endpoint(personal: PersonalCreate, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    created = await create_personal(personal, repository)
    return PersonalResponse(**created.model_dump())

@router.get("/{personal_id}", response_model=PersonalResponse)
async def read_personal(personal_id: str, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    person = await get_personal(personal_id, repository)
    if person is None:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    return PersonalResponse(**person.model_dump())

@router.get("/", response_model=List[PersonalResponse])
async def read_all_personal(db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    persons = await get_all_personal(repository)
    return [PersonalResponse(**p.model_dump()) for p in persons]

@router.put("/{personal_id}", response_model=PersonalResponse)
async def update_personal_endpoint(personal_id: str, personal: PersonalCreate, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    updated = await update_personal(personal_id, personal, repository)
    if updated is None:
        raise HTTPException(status_code=404, detail="Personal no encontrado")
    return PersonalResponse(**updated.__dict__)

@router.delete("/{personal_id}", response_model=dict)
async def delete_personal_endpoint(personal_id: str, db: AsyncSession = Depends(get_db)):
    repository = PersonalRepository(db)
    try:
        await delete_personal(personal_id, repository)
        return {"detail": "Registro de personal eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
