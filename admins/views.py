from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse

from users.models import Subscription


@user_passes_test(lambda u: u.is_superuser)
def overview(request):

    subscriptions = Subscription.objects.exclude(
        accepted=True, subscription=Subscription.USER
    )

    return render(
        request,
        "admins/overview.html",
        {
            "subscriptions": subscriptions,
        }
    )
