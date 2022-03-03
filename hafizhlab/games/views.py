from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from hafizhlab.games.models import GameSession
from hafizhlab.games.serializers import GameSessionSerializer


class GameSessionRetrieveAPIView(RetrieveAPIView):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer
    lookup_field = 'public_code'


class GameSessionAPIView(ListCreateAPIView):
    serializer_class = GameSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = {
            'challenge__{}'.format(key): self.request.query_params[key]
            for key in ('mode', 'scope_ct', 'scope_id')
        }
        return GameSession.objects.filter(**params)

    def create(self, request, *args, **kwargs):
        request.data['admin'] = request.user.pk
        return super().create(request, *args, **kwargs)
