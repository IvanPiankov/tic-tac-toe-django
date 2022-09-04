from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView



from tictactoe.models import Player, Match
from tictactoe.serializers import PlayerSerializer, MatchSerializer


class AddPlayer(APIView):
    def post(self, request):
        player, created = Player.objects.get_or_create(nickname=request.data['nickname'])
        return Response(PlayerSerializer(instance=player).data)


class StartMatch(APIView):
    def post(self, request):
        players_uuid = request.headers.get("Player-ID", None)
        player = get_object_or_404(Player, id=players_uuid)
        match = Match.objects.annotate(players_count=Count('players')).filter(started=False, players_count=1).first()
        if not match:
            match = Match.objects.create()
        match.players.add(player)
        return Response(MatchSerializer(instance=match).data)
