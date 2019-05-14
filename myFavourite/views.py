# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponse
import json
from myFavourite.models import *


# Create your views here.


def index(request):
    return HttpResponse("home")


def get_myfavourite(request):
    result = {'result': 0}

    try:
        discounts = []
        for d in MyFavourite.objects.all():
            myfavourite = {'StoreName': d.StoreName,
                           'DiscountName': d.DiscountName,
                           'Latitude': d.latitude,
                           'Longitude': d.longitude,
                           'Introduction': d.introduction}
            discounts.append(myfavourite)
        result['myfavourite'] = myfavourite
        result['result'] = 1 if len(discounts) > 0 else 0
    except Exception as e:
        result['message'] = str(e)
    return JsonResponse(result)