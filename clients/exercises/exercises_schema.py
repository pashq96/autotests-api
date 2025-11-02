from pydantic import BaseModel, Field, ConfigDict


class ExerciseSchema(BaseModel):
    """
    Описание структуры задания.
    """
    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class GetExercisesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка заданий курса.
    """
    course_id: str = Field(alias="courseId")


class CreateExercisesSchema(BaseModel):
    """
    Описание словаря на создание задания
    """
    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class UpdateExersisesSchema(BaseModel):
    """
    Описание словаря на обновление задания
    """
    title: str | None
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    order_index: int | None = Field(alias="orderIndex")
    description: str | None
    estimated_time: str | None = Field(alias="estimatedTime")


class GetExercisesResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение всех заданий курса
    """
    exercises: list[ExerciseSchema]


class GetExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение задания курса по id
    """
    exercise: ExerciseSchema
