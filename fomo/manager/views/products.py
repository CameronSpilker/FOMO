from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
@permission_required('catalog.change_product', login_url='/manager/permissions/')
def process_request(request):


    products = cmod.Product.objects.order_by('-create_date').all()



    context = {
        'products':products,
    }
    return dmp_render(request, 'products.html', context)

@view_function
@login_required(login_url='/account/login/')
@permission_required('catalog.delete_product', login_url='/manager/permissions/')
def get_quantity(request):
    #get the current quanitty of product id in url params[0]

    try:
        product = cmod.BulkProduct.objects.get(id=request.urlparams[0])#.get is for a single product
    except (TypeError, cmod.BulkProduct.DoesNotExist):
        return HttpResponseRedirect('/manager/products/')

    #return the quantity
    return HttpResponse(product.quantity)
