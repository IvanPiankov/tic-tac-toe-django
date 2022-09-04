from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from tictactoe.models import Player
from tictactoe.serializers import PlayerSerializer


class AddPlayer(APIView):
    def post(self, request):
        player, created = Player.objects.get_or_create(nickname=request.data['nickname'])
        return Response(PlayerSerializer(instance=player).data)

