from rest_framework import serializers

from tictactoe.models import Player, Match


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(read_only=True, many=True)

    class Meta:
        model = Match
        fields = '__all__'

