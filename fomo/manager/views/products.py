from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from .. import dmp_render, dmp_render_to_string

@view_function
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

    products = cmod.Product.objects.order_by('name').all()
    print('>>>', products)



    context = {
        'products':products,
    }
    return dmp_render(request, 'products.html', context)
