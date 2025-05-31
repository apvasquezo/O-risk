from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from infrastructure.orm.models import Evaluation
from domain.entities.Evaluation import Evaluation as EvaluationEntity

class EvaluationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_evaluation(self, evaluation:EvaluationEntity)->EvaluationEntity:
        stmt=insert(Evaluation).values(
            control_id=evaluation.control_id,
            event_id=evaluation.event_id,
            eval_date=evaluation.eval_date,
            n_probability=evaluation.n_probability,
            n_impact=evaluation.n_impact,
            personal_id = evaluation.personal_id,
            next_date = evaluation.next_date,
            description=evaluation.description,
            state=evaluation.state
        ).returning(
            Evaluation.id_evaluation,
            Evaluation.control_id,
            Evaluation.event_id,
            Evaluation.eval_date,
            Evaluation.n_probability,
            Evaluation.n_impact,
            Evaluation.personal_id,
            Evaluation.next_date,
            Evaluation.description,
            Evaluation.state
        )
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return EvaluationEntity(
                    id_evaluation=row.id_evaluation,
                    control_id=row.control_id,
                    event_id=row.event_id,
                    eval_date=row.eval_date,
                    n_probability=row.n_probability,
                    n_impact=row.n_impact,
                    personal_id = row.personal_id,
                    next_date = row.next_date,
                    description=row.description,
                    state=row.state                    
                )
        except IntegrityError as e:
            await self.session.rollback()
            raise ValueError ("Evaluation already exists") from e
    
    async def get_evaluation(self, evaluation_id:int)->Optional[EvaluationEntity]:
        stmt = select(Evaluation).where(Evaluation.id_evaluation == evaluation_id)
        result = await self.session.execute(stmt)
        evaluations= result.scalar_one_or_none()
        if evaluations:
            return EvaluationEntity(
                id_evaluation=evaluations.id_evaluation,
                control_id=evaluations.control_id,
                event_id=evaluations.event_id,
                eval_date=evaluations.eval_date,
                n_probability=evaluations.n_probability,
                n_impact=evaluations.n_impact,
                personal_id = evaluations.personal_id,
                next_date = evaluations.next_date,
                description=evaluations.description,
                state=evaluations.state                      
            )
        return None
    
    async def get_all_evaluation(self)-> List[EvaluationEntity]:
        stmt = select(Evaluation)
        result = await self.session.execute(stmt)
        evaluations = result.scalars().all()
        return [
            EvaluationEntity(
               id_evaluation=a.id_evaluation,
                control_id=a.control_id,
                event_id=a.event_id,
                eval_date=a.eval_date,
                n_probability=a.n_probability,
                n_impact=a.n_impact,
                personal_id = a.personal_id,
                next_date = a.next_date,
                description=a.description,
                state=a.state                 
            ) for a in evaluations
        ]     