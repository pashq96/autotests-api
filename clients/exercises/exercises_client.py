from httpx import Response

from clients.api_client import APIClient
from clients.api_coverage import tracker
from clients.exercises.exercises_schema import GetExercisesQuerySchema, GetExercisesResponseSchema, \
    GetExerciseResponseSchema, CreateExerciseRequestSchema, UpdateExersiseRequestSchema
from clients.private_http_builder import AuthenticationUserSchema, get_private_http_client
import allure

from tools.routes import APIRoutes


class ExercisesClient(APIClient):
    """
    Клиент для работы с /api/v1/exercises
    """

    @allure.step("Get exercises")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}")
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Метод получения всех заданий в курсе
        :param query: Словарь с id курса
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(
            APIRoutes.EXERCISES,
            params=query.model_dump(by_alias=True))

    @allure.step("Get exercise")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def get_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод получения урока по id

        :param exercise_id: id урока
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.get(f"{APIRoutes.EXERCISES}/{exercise_id}")

    @allure.step("Create exercise")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """
        Метод создания заданий

        :param request: Словарь title, courseId, maxScore, minScore, orderIndex, description, estimatedTime
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post(
            APIRoutes.EXERCISES,
            json=request.model_dump(by_alias=True))

    @allure.step("Update exercise")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def update_exercise_api(self, exercise_id: str, request: UpdateExersiseRequestSchema) -> Response:
        """
        Метод обновления данных задания

        :param exercise_id: id задания
        :param request: Словарь title, maxScore, minScore, orderIndex, description, estimatedTime
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.patch(f"{APIRoutes.EXERCISES}/{exercise_id}",
                          json=request.model_dump(by_alias=True, exclude_none=True))

    @allure.step("Delete exercise")
    @tracker.track_coverage_httpx(f"{APIRoutes.EXERCISES}/{{exercise_id}}")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """
        Метод удаления задания

        :param exercise_id: id задания
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.delete(f"{APIRoutes.EXERCISES}/{exercise_id}")

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise(self, exercise_id: str) -> GetExerciseResponseSchema:
        response = self.get_exercises_api(exercise_id)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> GetExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(self, exercise_id: str, request: UpdateExersiseRequestSchema) -> GetExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id, request)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    def delete_exercise(self, exercise_id: str) -> str:
        response = self.delete_exercise_api(exercise_id)
        return response.json()


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))
