from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from works.models import Works
from works.serializers import WorksSerializer, WorksRequestSerializer, WorksResponseSerializer
from rest_framework.views import APIView


class WorksView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        operation_summary="Получение списка всех статей",
        responses={200: WorksResponseSerializer(many=True), 500: "Серверная ошибка"},
    )
    def get(self, request):
        articles = Works.objects.all()
        serializer = WorksResponseSerializer(articles, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Создание новой статьи",
        request_body=WorksResponseSerializer,
        responses={
            201: WorksResponseSerializer,
            400: "Не правильный ввод данных",
            500: "Серверная ошибка",
        },
    )
    def post(self, request):
        if request.user is not None:
            serializer = WorksRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                authors = Works.objects.all()
                serializer = WorksResponseSerializer(authors, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class WorksDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @swagger_auto_schema(
        operation_summary="Получение информации о конкретной статье",
        responses={200: WorksResponseSerializer, 500: "Серверная ошибка"},
    )
    def get(self, request, pk):
        article = Works.objects.filter(pk=pk).first()
        serializer = WorksResponseSerializer(article)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Изменение данных статьи",
        responses={
            200: WorksResponseSerializer,
            400: "Не правильный ввод данных",
            500: "Серверная ошибка",
        },
        request_body=WorksRequestSerializer
    )
    def put(self, request, pk):
        article = Works.objects.filter(pk=pk).first()
        serializer = WorksResponseSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Удаление статьи",
        responses={204: WorksResponseSerializer, 500: "Серверная ошибка"},
    )
    def delete(self, request, pk):
        article = Works.objects.filter(pk=pk).first()
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
