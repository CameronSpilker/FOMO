from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from formlib.form import FormMixIn
from django import forms
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
@permission_required('account.change_fomouser', login_url='/manager/permissions/')
def process_request(request):


   history = request.user.product_history()




   context = {'history': history}

   return dmp_render(request, 'producthistory.html', context)
