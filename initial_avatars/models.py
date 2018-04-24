# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings


class Background(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        related_name='initial_avatars',
        on_delete=models.CASCADE
    )
    R = models.IntegerField()
    G = models.IntegerField()
    B = models.IntegerField()
