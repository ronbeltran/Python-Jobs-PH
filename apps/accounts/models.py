
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime

from django.db.models import signals
from accounts.signals import create_profile


class UserProfile(models.Model):

    BANNED = 1
    FRIEND = 2
    STATUS_CHOICES = (
        (BANNED, 'Banned'),
        (FRIEND, 'Friend'),
    )

    user = models.ForeignKey(User, unique=True)
    url = models.URLField(verify_exists=False, blank=True,
        help_text=_('Website. This field is optional.'))
    trusted = models.BooleanField(default=False)
#    role = models.IntegerField(choices=STATUS_CHOICES, default=JOB_POSTER,
#        help_text=_("Please specify if you're a job poster or seeker."))


    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })

    get_absolute_url = models.permalink(get_absolute_url)


# When model instance is saved, trigger creation of corresponding profile
signals.post_save.connect(create_profile, sender=User)


