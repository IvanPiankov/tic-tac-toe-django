from django.urls import re_path

from tictactoe.consumers import MatchConsumer

websocket_urlpatterns = [
    re_path(r'match/(?P<match_id>.+)/$', MatchConsumer.as_asgi()),
]