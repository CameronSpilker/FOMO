from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
def process_request(request):
    currentuser = request.user
    fomouser = amod.FomoUser.objects.get(id=currentuser.id)
    print('>>>', fomouser)



    context = {
        'fomouser':fomouser,
    }
    return dmp_render(request, 'myinfo.html', context)
