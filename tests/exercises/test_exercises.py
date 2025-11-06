from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from clients.errors_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExersiseRequestSchema, UpdateExersiseResponseSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@pytest.mark.exercises
@pytest.mark.regression
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
class TestExercises:
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Create exercise")
    def test_create_exercise(self, function_course: CourseFixture, exercises_client: ExercisesClient):
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercises_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(response_data, request)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Get exercise")
    def test_get_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        response = exercises_client.get_exercise_api(exercise_id=function_exercise.response.exercise.id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(response_data, function_exercise.response)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.title("Update exercise")
    def test_update_exercise(self,
                             function_exercise: ExerciseFixture,
                             exercises_client: ExercisesClient
                             ):
        request = UpdateExersiseRequestSchema(
            title=fake.sentence(),
            max_score=None,
            min_score=None,
            order_index=None,
            description=None,
            estimated_time=None
        )
        response = exercises_client.update_exercise_api(
            exercise_id=function_exercise.response.exercise.id,
            request=request
        )
        response_data = UpdateExersiseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(response_data, request)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Delete exercise")
    def test_delete_exercise(self,
                             function_exercise: ExerciseFixture,
                             exercises_client: ExercisesClient
                             ):
        response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)

        assert_status_code(response.status_code, HTTPStatus.OK)

        response_error = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        response_error_data = InternalErrorResponseSchema.model_validate_json(response_error.text)

        assert_status_code(response_error.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(response_error_data)
        validate_json_schema(response_error.json(), response_error_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Get exercises")
    def test_get_exercises(self,
                           function_exercise: ExerciseFixture,
                           exercises_client: ExercisesClient,
                           function_course: CourseFixture
                           ):
        request = GetExercisesQuerySchema(course_id=function_course.response.course.id)
        response = exercises_client.get_exercises_api(request)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercises_response(response_data, [function_exercise.response])
        validate_json_schema(response.json(), response_data.model_json_schema())
