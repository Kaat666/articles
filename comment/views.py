from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from comment.models import Comment
from comment.serializers import CommentSerializer, CommentRequestSerializer, CommentResponseSerializer
from rest_framework.views import APIView


class WorksView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        operation_summary="Получение списка всех комментариев",
        responses={200: CommentResponseSerializer(many=True), 500: "Серверная ошибка"},
    )
    def get(self, request):
        comment = Comment.objects.all()
        serializer = CommentResponseSerializer(comment, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Создание нового комментария",
        request_body=CommentResponseSerializer,
        responses={
            201: CommentResponseSerializer,
            400: "Не правильный ввод данных",
            500: "Серверная ошибка",
        },
    )
    def post(self, request):
        if request.user is not None:
            serializer = CommentRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                authors = Comment.objects.all()
                serializer = CommentResponseSerializer(authors, many=True)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class WorksDetailView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @swagger_auto_schema(
        operation_summary="Получение информации о конкретном комментарии",
        responses={200: CommentResponseSerializer, 500: "Серверная ошибка"},
    )
    def get(self, request, pk):
        comment = Comment.objects.filter(pk=pk).first()
        serializer = CommentResponseSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Изменение комментария",
        responses={
            200: CommentResponseSerializer,
            400: "Не правильный ввод данных",
            500: "Серверная ошибка",
        },
        request_body=CommentRequestSerializer
    )
    def put(self, request, pk):
        comment = Comment.objects.filter(pk=pk).first()
        serializer = CommentResponseSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Удаление комментария",
        responses={204: CommentResponseSerializer, 500: "Серверная ошибка"},
    )
    def delete(self, request, pk):
        comment = Comment.objects.filter(pk=pk).first()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

