from datetime import timedelta, datetime
from collections import OrderedDict

from django.utils import timezone
from django.contrib.auth.models import User

from .users import Subscription, Leadership, Profile
from apis.models import Api


def create_related(self):
    #Profile.objects.create(user=self)
    Subscription.objects.create(
        user=self,
        accepted=True,
        wallet=1000000,
        category=Subscription.USER,
        subscription=Subscription.FREE,
    )


#return list of inactive users
@staticmethod
def inactive_dict():
    users = User.objects.order_by("username")
    temp = OrderedDict()
    for user in users:
        if user.is_inactive():
            temp[user.username] = user.days_since_last_login()
    return temp


#see when user is inactive
def is_inactive(self):
    now = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(days=30)
    if now > self.last_login.replace(tzinfo=timezone.utc):
        return False
    else:
        return True


#see how long ago a user last logged in
def days_since_last_login(self):
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    delta = now - self.last_login.replace(tzinfo=timezone.utc)
    if delta.days == 0:
        return "Today"
    else:
        return "%d days ago" % delta.days


# check if user has access to corporation settings
def corporation_access(self):
    if Leadership.objects.filter(
        director=self, account__category=Subscription.CORPORATION
    ).exists():
        return True
    elif Subscription.objects.filter(
        user=self, category=Subscription.CORPORATION
    ):
        return True


def alliance_access(self):
    if Leadership.objects.filter(
        director=self, account__category=Subscription.ALLIANCE
    ).exists():
        return True
    elif Subscription.objects.filter(
        user=self, category=Subscription.ALLIANCE
    ):
        return True


def coalition_access(self):
    if Leadership.objects.filter(
        director=self, account__category=Subscription.COALITION
    ).exists():
        return True
    elif Subscription.objects.filter(
        user=self, category=Subscription.COALITION
    ):
        return True


def has_characters(self):
    return Api.objects.filter(user=self).exclude(
        accounttype=Api.CORPORATION
    ).exists()


def all_characters(self):
    characters = []
    apis = Api.objects.filter(user=self).exclude(
        accounttype=Api.CORPORATION
    )
    for api in apis:
        characters += list(api.characterapi_set.all())
    return characters


User.add_to_class("create_related", create_related)
User.add_to_class("is_inactive", is_inactive)
User.add_to_class("days_since_last_login", days_since_last_login)
User.add_to_class("inactive_dict", inactive_dict)
User.add_to_class("corporation_access", corporation_access)
User.add_to_class("alliance_access", alliance_access)
User.add_to_class("coalition_access", coalition_access)
User.add_to_class("has_characters", has_characters)
User.add_to_class("all_characters", all_characters)
