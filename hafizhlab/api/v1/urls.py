from django.urls import include, path

from hafizhlab.games.views import GameSessionAPIView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),

    path('games/', GameSessionAPIView.as_view(), name='game-list'),
]
