from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
@permission_required('account.change_fomouser', login_url='/manager/permissions/')
def process_request(request):
    #query all products
    # .all()
    # .filter(name='trumpet')
    # .exclude()
    #(List of products)
    ###################.get(id=12334) -- you only get one thing back
    #try:
        #.get(id=1234)
    #except cmod.Product.DoesNotExist:
        #what now?
        #return HttpResponseRedirect('/manager/products/')

    fomouser = amod.FomoUser.objects.order_by('username').all()
    print('>>>', fomouser)



    context = {
        'fomouser':fomouser,
    }
    return dmp_render(request, 'edituserstable.html', context)
