from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from hafizhlab.games.models import GameSession
from hafizhlab.games.serializers import GameSessionSerializer


class GameSessionAPIView(ListCreateAPIView):
    serializer_class = GameSessionSerializer
    queryset = GameSession.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['admin'] = request.user.pk
        return super().create(request, *args, **kwargs)
