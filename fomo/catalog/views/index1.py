from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from django.contrib.auth.decorators import login_required, permission_required
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

    products = cmod.Product.objects.order_by().all()
    # picture = cmod.ProductPicture.objects.all()
    category = cmod.Category.objects.order_by('name')
 
    print('>>>?F<SEDLJFIOEHFUI(H*(EBFU', request.last5)


    last5 = cmod.Product.objects.filter(id__in=request.last5)
    print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', last5)


    context = {
        'products': products,
        'category': category,
        'last5': last5,
        # 'picture': picture,
    }
    return dmp_render(request, 'index1.html', context)


@view_function
def get_cat(request):
    #get the current quanitty of product id in url params[0]
    try:
        print(request.urlparams[0])
        category = cmod.Category.objects.order_by('name')#.get is for a single product
        products = cmod.Product.objects.filter(category=request.urlparams[0])
        print('>>>>>>>>>>', category)
        print('>>>>>>>>>>', products)
    except (TypeError, cmod.Category.DoesNotExist):
        return HttpResponseRedirect('/catalog/index1/')

        
    last5 = cmod.Product.objects.filter(id__in=request.last5)
    print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', last5)

    print('>>>>>>>>>>', category)
    context = { 
        'category': category,
        'products': products,
        'last5': last5,
    }
    return dmp_render(request, 'index1.html', context)


# @view_function
# def search_bar(request):
#     #get the current quanitty of product id in url params[0]
#     try:
#         print(request.urlparams[0])
#         category = cmod.Category.objects.order_by('name')#.get is for a single product
#         products = cmod.Product.objects.filter(desc__icontains=request.urlparams[0])
#         print('>>>>>>>>>>', category)
#         print('>>>>>>>>>>', products)
#     except (TypeError, cmod.Product.DoesNotExist):
#         return HttpResponseRedirect('/catalog/index1/')

        
#     last5 = cmod.Product.objects.filter(id__in=request.last5)
#     print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', last5)

#     print('>>>>>>>>>>', category)
#     context = { 
#         'category': category,
#         'products': products,
#         'last5': last5,
#     }
#     return dmp_render(request, 'searchresults.html', context)