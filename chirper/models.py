from django.db import models
from django.conf import settings
from django_stormpath.models import StormpathUser

class Chirp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    message = models.TextField(max_length=160, verbose_name='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class ChirperUser(StormpathUser):

    def is_admin(self):
        return True
