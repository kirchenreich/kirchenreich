from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


def generate():
    key = User.objects.make_random_password(length=40)
    while ApiKey.objects.filter(key__exact=key).count():
        key = User.objects.make_random_password(length=KEY_SIZE)
    return key


class ApiKey(models.Model):
    user = models.ForeignKey(User, related_name='keys')
    key = models.CharField(max_length=40, unique=True, blank=True,
                           default=generate)
    last_ip = models.CharField(max_length=32, blank=True, null=True,
                               default=None)
    last_used = models.DateTimeField(blank=True, null=True, default=None)
    created = models.DateTimeField(default=datetime.utcnow)

    notes = models.TextField(blank=True, null=True,
                             default=None)

    class Meta:
        ordering = ['-created']

    def login(self, ip_address):
        self.last_ip = ip_address
        last_used = datetime.utcnow()
        self.save()

    def __unicode__(self):
        return 'ApiKey: %s, %s [%s, %s]' % (self.user, self.key,
                                            self.last_ip, self.last_used)
