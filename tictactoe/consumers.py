import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Count

from tictactoe.models import Match


@database_sync_to_async
def get_match(match_id: str):
    return Match.objects.get(id=match_id)


@database_sync_to_async
def get_players_count(match_id: str):
    return Match.objects.annotate(players_count=Count('players')).filter(id=match_id).first()


@database_sync_to_async
def add_player_to_match(match: str, player):
    match.players.add(player)


class MatchConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        match_id = self.scope['url_route']['kwargs']['match_id']
        match = await get_match(match_id)
        if match.started:
            raise Exception("Already started match")
        players = await get_players_count(match_id)
        if players.players_count.players_count > 1:
            raise Exception('Too many players')
        await add_player_to_match(match_id, self.scope['player'])
        self.match_group_name = 'match_%s' % match_id
        await self.channel_layer.group_add(self.match_group_name,
                                           self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.match_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.match_group_name, {
                'type': 'send_message',
                'message': message,
                "event": "MOVE"
            })

        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.match_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "START"
            })

        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.match_group_name, {
                'type': 'send_message',
                'message': message,
                'event': "END"
            })

    async def send_message(self, message):
        """ Receive message from room group """
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
        }))
