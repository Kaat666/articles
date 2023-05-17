from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from author.models import Author
from author.serializers import AuthorSerializer, AuthorRequestSerializer, AuthorResponseSerializer
from rest_framework.views import APIView


class AuthorView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Получение списка всех пользователей",
        responses={200: AuthorResponseSerializer(many=True), 500: "Серверная ошибка"},
    )
    def get(self, request):
        authors = Author.objects.all()
        serializer = AuthorResponseSerializer(authors, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Создание нового пользователя",
        request_body=AuthorResponseSerializer,
        responses={
            201: AuthorResponseSerializer,
            400: "Не правильный ввод данных",
            500: "Серверная ошибка",
        },
    )
    def post(self, request):
        serializer = AuthorRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            authors = Author.objects.all()
            serializer = AuthorResponseSerializer(authors, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Получение информации о конкретном пользователе",
        responses={200: AuthorResponseSerializer, 500: "Серверная ошибка"},
    )
    def get(self, request, pk):
        author = Author.objects.filter(pk=pk).first()
        serializer = AuthorResponseSerializer(author)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Изменение данных пользователя",
        responses={
            200: AuthorResponseSerializer,
            400: "Не правильный ввод данных",
            500: "Серверная ошибка",
        },
        request_body=AuthorRequestSerializer
    )
    def put(self, request, pk):
        author = Author.objects.filter(pk=pk).first()
        serializer = AuthorResponseSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Удаление пользователя",
        responses={204: AuthorResponseSerializer, 500: "Серверная ошибка"},
    )
    def delete(self, request,pk):
        author = Author.objects.filter(pk=pk).first()
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
