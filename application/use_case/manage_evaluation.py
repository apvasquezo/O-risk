from domain.entities.Evaluation import Evaluation
from domain.repositories.evaluation_repository import EvaluationRepository

async def create_evaluations(eval_data: Evaluation, repository: EvaluationRepository) -> Evaluation:
    return await repository.create_evaluation(eval_data)

async def get_evaluations(control_id: int, repository: EvaluationRepository) -> Evaluation:
    return await repository.get_cevaluation(control_id)

async def get_all_evaluations(repository: EvaluationRepository) -> list[Evaluation]:
    return await repository.get_all_evaluation()

async def update_evaluations(control_id: int, control_data: Evaluation, repository: EvaluationRepository) -> Evaluation:
    return await repository.update_control(control_id, control_data)

async def delete_evaluations(eval_id: int, repository: EvaluationRepository) -> None:
    await repository.delete_evaluation(eval_id)