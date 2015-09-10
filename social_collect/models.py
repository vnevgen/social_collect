__author__ = 'vitaly'


from django.db import models
from django.utils.translation import ugettext_lazy as _

TYPES_CHOICES = (
    ("twitter", _("Twitter")),
    ("vk", _("VKontakte")),
    ("instagram", _("Instagram"))
)

class Person(models.Model):
    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

    @property
    def image(self):
        try:
            return self.accounts.get(use_image=True).image
        except PersonAccount.DoesNotExist:
            # if not selected desired image
            return self.accounts.first().image  # if  returns None


class PersonAccount(models.Model):
    person = models.ForeignKey(Person, related_name='accounts', blank=False)
    type = models.CharField(max_length=20, choices=TYPES_CHOICES, blank=False)
    screen_name = models.CharField(max_length=255, blank=False)
    social_id = models.CharField(max_length=255, blank=False)

    name = models.CharField(max_length=255, blank=True)
    image = models.CharField(max_length=255, blank=True)
    use_image = models.BooleanField(default=False)

    class Meta:
        unique_together = (('type', 'social_id'),)

    def set_use_image(self):
        self.person.accounts.all().update(use_image=False)
        self.use_image = True

    def __str__(self):
        return "%s: %s (%s) by %s" % (self.type, self.screen_name, self.social_id, self.person.name)