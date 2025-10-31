from typing import TypedDict, List
from httpx import Response

from clients.api_client import APIClient
from clients.private_http_builder import AuthenticationUserDict, get_private_http_client


class ExerciseDict(TypedDict):
    """
    Описание структуры задания.
    """
    id: str
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class GetExercisesQueryDict(TypedDict):
    """
    Описание структуры запроса на получение списка заданий курса.
    """
    courseId: str


class CreateExercisesDict(TypedDict):
    """
    Описание словаря на создание задания
    """
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class UpdateExersisesDict(TypedDict):
    """
    Описание словаря на обновление задания
    """
    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None


class GetExercisesResponseDict(TypedDict):
    """
    Описание структуры ответа на получение всех заданий курса
    """
    exercises: List[ExerciseDict]


class GetExerciseResponseDict(TypedDict):
    """
    Описание структуры ответа на получение задания курса по id
    """
    exercise: ExerciseDict


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """
        Метод получения всех заданий в курсе
        :param query: Словарь с id курса
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения урока по id

        :param exercise_id: id урока
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExercisesDict) -> Response:
        """
        Метод создания заданий

        :param request: Словарь title, courseId, maxScore, minScore, orderIndex, description, estimatedTime
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExersisesDict) -> Response:
        """
        Метод обновления данных задания

        :param exercise_id: id задания
        :param request: Словарь title, maxScore, minScore, orderIndex, description, estimatedTime
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления задания

        :param exercise_id: id задания
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
        response = self.get_exercises_api(query)
        return response.json()

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseDict:
        response = self.get_exercises_api(exercise_id)
        return response.json()

    def create_exercise(self, request: CreateExercisesDict) -> GetExerciseResponseDict:
        response = self.create_exercise_api(request)
        return response.json()

    def update_exercise(self, exercise_id: str, request: UpdateExersisesDict) -> GetExerciseResponseDict:
        response = self.update_exercise_api(exercise_id, request)
        return response.json()

    def delete_exercise(self, exercise_id: str) -> str:
        response = self.delete_exercise_api(exercise_id)
        return response.json()


def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))
