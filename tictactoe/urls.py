from django.urls import path, include

from tictactoe.views import AddPlayer

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('players/join/', AddPlayer.as_view()),
]
