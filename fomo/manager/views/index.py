from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from formlib.form import FormMixIn
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
@permission_required('account.add_fomouser', login_url='/account/index/')
@permission_required('catalog.add_product', login_url='/account/index/')
def process_request(request):


    return dmp_render(request, 'index.html')
