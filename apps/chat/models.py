from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    from_who = models.ForeignKey(User, on_delete=models.PROTECT, related_name='from_user', default=None)
    to_who = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to_user', default=None)
    message = models.TextField()
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    has_been_seen = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.message


class UserChannel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    channel_name = models.TextField()

    def __str__(self):
        return self.channel_name


