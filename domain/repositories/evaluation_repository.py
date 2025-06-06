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
        print("entramos al repositorio")
        stmt=insert(Evaluation).values(
            eventlog_id=evaluation.eventlog_id,            
            control_id=evaluation.control_id,
            eval_date=evaluation.eval_date,
            n_probability=evaluation.n_probability,
            n_impact=evaluation.n_impact,
            next_date = evaluation.next_date,
            description=evaluation.description,
            observation=evaluation.observation,
            state_control=evaluation.state_control,
            state_evaluation=evaluation.state_evaluation,
            control_efficiency=evaluation.control_efficiency,
            created_by=evaluation.created_by,
        ).returning(
            Evaluation.id_evaluation,
            Evaluation.eventlog_id,            
            Evaluation.control_id,
            Evaluation.eval_date,
            Evaluation.n_probability,
            Evaluation.n_impact,
            Evaluation.next_date,
            Evaluation.description,
            Evaluation.observation,
            Evaluation.state_control,
            Evaluation.state_evaluation,
            Evaluation.control_efficiency,
            Evaluation.created_by,
        )
        print("lo que se va a guardar ", stmt)
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()
            row=result.fetchone()
            if row:
                return EvaluationEntity(
                    id_evaluation=row.id_evaluation,
                    eventlog_id=row.eventlog_id,                    
                    control_id=row.control_id,
                    eval_date=row.eval_date,
                    n_probability=row.n_probability,
                    n_impact=row.n_impact,
                    next_date = row.next_date,
                    description=row.description,
                    observation=row.observation,
                    state_control=row.state_control,
                    state_evaluation=row.state_evaluation,
                    control_efficiency=row.control_efficiency,
                    created_by=row.created_by,                    
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
                eventlog_id=evaluations.eventlog_id,                
                control_id=evaluations.control_id,
                eval_date=evaluations.eval_date,
                n_probability=evaluations.n_probability,
                n_impact=evaluations.n_impact,
                next_date = evaluations.next_date,
                description=evaluations.description,
                observation=evaluations.observation,
                state_control=evaluations.state_control,
                state_evaluation=evaluations.state_evaluation,
                control_efficiency=evaluations.control_efficiency,
                created_by=evaluations.created_by,                   
            )
        return None
    
    async def get_all_evaluation(self)-> List[EvaluationEntity]:
        stmt = select(Evaluation)
        result = await self.session.execute(stmt)
        evaluations = result.scalars().all()
        return [
            EvaluationEntity(
               id_evaluation=a.id_evaluation,
                eventlog_id=a.eventlog_id,               
                control_id=a.control_id,
                eval_date=a.eval_date,
                n_probability=a.n_probability,
                n_impact=a.n_impact,
                next_date = a.next_date,
                description=a.description,
                observation=a.observation,
                state_control=a.state_control,
                state_evaluation=a.state_evaluation,
                control_efficiency=a.control_efficiency,
                created_by=a.created_by,               
            ) for a in evaluations
        ]
        
    async def update_evaluation(self, evaluation_id:int, eval:EvaluationEntity) -> Optional[EvaluationEntity]:
        stmt=update(Evaluation).where(Evaluation.id_evaluation == evaluation_id).values(
            eventlog_id=eval.eventlog_id,               
            control_id=eval.control_id,
            eval_date=eval.eval_date,
            n_probability=eval.n_probability,
            n_impact=eval.n_impact,
            next_date = eval.next_date,
            description=eval.description,
            observation=eval.observation,
            state_control=eval.state_control,
            state_evaluation=eval.state_evaluation,
            control_efficiency=eval.control_efficiency,
            created_by=eval.created_by,                    
        ). returning(
            Evaluation.id_evaluation,
            Evaluation.eventlog_id,               
            Evaluation.control_id,
            Evaluation.eval_date,
            Evaluation.n_probability,
            Evaluation.n_impact,
            Evaluation.next_date,
            Evaluation.description,
            Evaluation.observation,
            Evaluation.state_control,
            Evaluation.state_evaluation,
            Evaluation.control_efficiency,
            Evaluation.created_by,            
        )
        result= await self.session.execute(stmt)
        await self.session.commit()
        row=result.fetchone()
        if row:
            return EvaluationEntity(
                id_evaluation=row.id_evaluation,
                eventlog_id=row.eventlog_id,               
                control_id=row.control_id,
                eval_date=row.eval_date,
                n_probability=row.n_probability,
                n_impact=row.n_impact,
                next_date = row.next_date,
                description=row.description,
                observation=row.observation,
                state_control=row.state_control,
                state_evaluation=row.state_evaluation,
                control_efficiency=row.control_efficiency,
                created_by=row.created_by,                 
            )
        return None
    
    async def delete_evaluation(self, eval_id:int) -> None:
        stmt=delete(Evaluation).where(Evaluation.id_evaluation==eval_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        if result.rowcount==0:
            raise ValueError(f"Evaluation with id {eval_id} not found")