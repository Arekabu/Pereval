from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PerevalSerializer, PerevalDetailSerializer
from .models import Pereval


class SubmitDataView(APIView):
    def get(self, request, pk=None):
        """
        Обрабатывает два типа GET-запросов:
        1. GET /submitData/?user__email=<email> - список перевалов пользователя
        2. GET /submitData/<pk>/ - детали конкретного перевала
        """

        if pk is None:
            # Обработка GET /submitData/?user__email=<email>
            email = request.query_params.get('user__email')
            if not email:
                return Response(
                    {"error": "Не указан email пользователя"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            perevals = Pereval.objects.filter(user__email=email).select_related('user', 'coords').prefetch_related(
                'images')
            serializer = PerevalDetailSerializer(perevals, many=True)
            return Response(serializer.data)
        else:
            # Обработка GET /submitData/<pk>/
            try:
                pereval = Pereval.objects.select_related('user', 'coords').prefetch_related('images').get(pk=pk)
                serializer = PerevalDetailSerializer(pereval)
                return Response(serializer.data)
            except Pereval.DoesNotExist:
                return Response(
                    {"message": "Перевал не найден", "id": pk},
                    status=status.HTTP_404_NOT_FOUND
                )

    def post(self, request):
        """Обработка POST /submitData/ - создание нового перевала"""

        serializer = PerevalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Запись успешно создана',
                    'id': serializer.instance.id
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'message': serializer.errors,
                'id': None
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        """Обработка PATCH /submitData/<pk>/ - обновление перевала"""

        try:
            pereval = Pereval.objects.select_related('user', 'coords').prefetch_related('images').get(pk=pk)
        except Pereval.DoesNotExist:
            return Response(
                {
                    'state': 0,
                    'message': 'Перевал не найден'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем статус - редактировать можно только 'new'
        if pereval.status != 'new':
            return Response(
                {
                    'state': 0,
                    'message': 'Редактирование запрещено: запись не в статусе "new"'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, чтобы не меняли данные пользователя
        if 'user' in request.data:
            user_data = request.data['user']
            current_user = pereval.user
            protected_fields = ['fam', 'name', 'otc', 'email', 'phone']

            for field in protected_fields:
                if field in user_data and user_data[field] != getattr(current_user, field):
                    return Response(
                        {
                            'state': 0,
                            'message': f'Редактирование поля {field} пользователя запрещено'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
            # Удаляем данные пользователя из request.data, чтобы сериализатор их не обрабатывал
            request.data.pop('user')

        # Обновляем данные
        serializer = PerevalSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'state': 1,
                    'message': 'Запись успешно обновлена'
                },
                status=status.HTTP_200_OK
            )

        # Если ошибка
        return Response(
            {
                'state': 0,
                'message': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
