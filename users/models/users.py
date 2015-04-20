from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from taggit.managers import TaggableManager


class Profile(models.Model):
    """ User profile. """

    AMERICA = "USA"
    AUSTRALIA = "AUS"
    EUROPE = "EU"
    TIMEZONES = (
        (AMERICA, "American"),
        (AUSTRALIA, "Australian"),
        (EUROPE, "European"),
    )

    user = models.OneToOneField(User)
    avatar = models.OneToOneField('characters.CharacterApi', null=True)
    country = CountryField(blank=True, blank_label='select country')
    timezone = models.CharField(max_length=3, choices=TIMEZONES, blank=True)
    tags = TaggableManager()

    def __unicode__(self):
        return "Profile of %s" % self.user.username

    def avatar_url(self):
        if self.avatar:
            return self.avatar.icon_special().url
        return "/static/images/default_avatar.jpg"


class Subscription(models.Model):
    """
    Unlocking options for leadership. Also used for settings like
    access, contact information and more
    """

    FREE = 0
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    SUBSCRIPTIONS = (
        (FREE, "Free"),
        (BRONZE, "Bronze"),
        (SILVER, "Silver"),
        (GOLD, "Gold"),
    )

    USER = 0
    CORPORATION = 1
    ALLIANCE = 2
    COALITION = 3
    CATEGORIES = (
        (USER, "User"),
        (CORPORATION, "Corporation"),
        (ALLIANCE, "Alliance"),
        (COALITION, "Coalition"),
    )

    user = models.ForeignKey(User)
    accepted = models.BooleanField(default=False)
    wallet = models.IntegerField(default=1000000)
    category = models.IntegerField(choices=CATEGORIES, default=USER)
    subscription = models.IntegerField(choices=SUBSCRIPTIONS, default=FREE)
    start_date = models.DateField(null=True)

    # corporation and alliance have to be validated by admin
    # name of corporation/alliance/coalition
    name = models.CharField(max_length=254, unique=True, null=True)
    #alliance/corporation id
    key = models.BigIntegerField(null=True)

    def __unicode__(self):
        return "%s: %s - %s" % (
            self.user.username,
            self.get_category_display(),
            self.get_subscription_display(),
        )


#only for corporation/alliance/coaltion memberships
class Leadership(models.Model):
    """ appointed directors that should have acces to the account pannel """

    account = models.ForeignKey("users.Subscription")
    director = models.ForeignKey(User)

    class Meta:
        unique_together = ["account", "director"]

    def __unicode__(self):
        return "%s: %s" % (self.account.name, self.director.username)
