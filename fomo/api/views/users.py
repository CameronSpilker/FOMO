from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from account import models as amod
from catalog import models as cmod
import json

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # qry = cmod.Product.objects
    # if min_price:
    #     qry = qry.filter(price__lte=min_price)
    # if max_price:
    #     qry = qry.filter(price__)

    # for p in qry:


    try:
        user = amod.FomoUser.objects.get(id=request.urlparams[0])
    except amod.FomoUser.DoesNotExist:
        return HttpResponseNotFound('Bad user id')


    ret = {

        'firstname': user.first_name,
        'lastname': user.last_name,
        'email': user.email,
        'username': user.username,
        'groups': [],

    }

    for g in user.groups.all():
        ret['groups'].append(g.name)

    return JsonResponse(ret)
    # return HttpResponse(json.dumps(ret), content_type="application/json")
    #postman is just a browser
