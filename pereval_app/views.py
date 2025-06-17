from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PerevalSerializer, PerevalDetailSerializer
from .models import Pereval


class SubmitDataView(APIView):
    def post(self, request):
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


class PerevalDetailView(RetrieveAPIView):
    serializer_class = PerevalDetailSerializer
    queryset = Pereval.objects.select_related('user', 'coords').prefetch_related('images')

    def get_object(self):
        try:
            return self.queryset.get(pk=self.kwargs['pk'])
        except Pereval.DoesNotExist:
            raise NotFound({'message': 'Перевал не найден', 'id': self.kwargs['pk']})
