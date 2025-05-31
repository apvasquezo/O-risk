from domain.entities.Probability import Probability
from domain.repositories.probability_repository import ProbabilityRepository

async def create_probability(probability_data: Probability, repository: ProbabilityRepository) -> Probability:
    return await repository.create_probability(probability_data)

async def get_probability(probability_id: int, repository: ProbabilityRepository) -> Probability:
    return await repository.get_probability(probability_id)

async def get_all_probabilities(repository: ProbabilityRepository) -> list[Probability]:
    return await repository.get_all_probabilities()

async def update_probability(probability_id: int, probability_data: Probability, repository: ProbabilityRepository) -> Probability:
    return await repository.update_probability(probability_id, probability_data)

async def delete_probability(probability_id: int, repository: ProbabilityRepository) -> None:
    await repository.delete_probability(probability_id)