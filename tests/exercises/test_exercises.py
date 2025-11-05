from http import HTTPStatus

import pytest

from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExersiseRequestSchema, UpdateExersiseResponseSchema
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@pytest.mark.exercises
@pytest.mark.regression
class TestExercises:
    def test_create_exercise(self, function_course: CourseFixture, exercises_client: ExercisesClient):
        request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercises_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(response_data, request)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_exercise(self, function_exercise: ExerciseFixture, exercises_client: ExercisesClient):
        response = exercises_client.get_exercise_api(exercise_id=function_exercise.response.exercise.id)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(response_data, function_exercise.response)
        validate_json_schema(response.json(), response_data.model_json_schema())

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
