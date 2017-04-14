from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):
    products = cmod.Product.objects.order_by().all()
    # picture = cmod.ProductPicture.objects.all()
    category = cmod.Category.objects.order_by('name')


    context = {
        'products': products,
        'category': category,
    }
    return dmp_render(request, 'index.html', context)


@view_function
def get_cat(request):
    #get the current quanitty of product id in url params[0]
    try:
        print(request.urlparams[0])
        category = cmod.Category.objects.order_by('name')  #.get is for a single product
        products = cmod.Product.objects.filter(category=request.urlparams[0])
    except (TypeError, cmod.Category.DoesNotExist):
        return HttpResponseRedirect('/catalog/index/')


    # last5 = cmod.Product.objects.filter(id__in=request.last5)
    # print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', last5)
    print('>>>>>>>>>>', category)
    last5 = 0
    if request.user.is_authenticated:
        last5 = request.user.last5()
        print('>>>>>>>>>>', category)
    context = { 
        'category': category,
        'products': products,
        'last5': last5,
    }
    return dmp_render(request, 'index.html', context)
