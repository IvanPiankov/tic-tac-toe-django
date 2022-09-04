from django.urls import path, include

from tictactoe.views import AddPlayer, StartMatch

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('players/join/', AddPlayer.as_view()),
    path('match/start', StartMatch.as_view())
]
