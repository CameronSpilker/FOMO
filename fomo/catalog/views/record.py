from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from catalog import models as cmod
from account import models as amod
from django.contrib.auth.decorators import login_required, permission_required

import stripe

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):

 sale = request.user.record_sale('monkey')

 return dmp_render(request, 'record.html', {'sale': sale})
