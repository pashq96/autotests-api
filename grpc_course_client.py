import grpc

import course_service_pb2  # Сгенерированные классы для работы с gRPC-сообщениями
import course_service_pb2_grpc  # Сгенерированный класс для работы с сервисом

# Устанавливаем соединение с сервером
channel = grpc.insecure_channel('localhost:50051')
stub = course_service_pb2_grpc.CourseServiceStub(channel)

# Отправляем запрос
response = stub.GetCourse(course_service_pb2.GetCourseRequest(course_id="Практика работы с gRPC протоколом"))
print(response)
