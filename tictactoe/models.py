import uuid

from django.db import models


class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=35, unique=True)


class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    players = models.ManyToManyField(Player)
    started = models.BooleanField(default=False)

# TODO: Think how to transfer Match to redis or another NoSQL

