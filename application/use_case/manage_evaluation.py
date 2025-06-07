from domain.entities.Evaluation import Evaluation
from domain.repositories.evaluation_repository import EvaluationRepository

async def create_evaluations(eval_data: Evaluation, repository: EvaluationRepository) -> Evaluation:
    return await repository.create_evaluation(eval_data)

async def get_evaluations(eval_id: int, repository: EvaluationRepository) -> Evaluation:
    return await repository.get_cevaluation(eval_id)

async def get_all_evaluations(repository: EvaluationRepository) -> list[Evaluation]:
    return await repository.get_all_evaluation()

async def update_evaluations(eval_id: int, eval_data: Evaluation, repository: EvaluationRepository) -> Evaluation:
    return await repository.update_evaluation(eval_id, eval_data)

async def delete_evaluations(eval_id: int, repository: EvaluationRepository) -> None:
    await repository.delete_evaluation(eval_id)