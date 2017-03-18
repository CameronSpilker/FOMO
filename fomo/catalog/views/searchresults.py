from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string
from django.contrib.postgres.search import SearchVector

@view_function
def process_request(request):
    #get the current quanitty of product id in url params[0]
    try:
        print(request.urlparams[0])
        userSearch = request.urlparams[0]
        category = cmod.Category.objects.order_by('name')#.get is for a single product
        products = cmod.Product.objects.annotate(search=SearchVector('desc') + SearchVector('name')).filter(search__icontains=userSearch)
        print('>>>>>>>>>>', category)
        print('>>>>>>>>>>', products)
    except (TypeError, cmod.Product.DoesNotExist):
        return HttpResponseRedirect('/catalog/index1/')


    last5 = cmod.Product.objects.filter(id__in=request.last5)
    print('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD', last5)

    print('>>>>>>>>>>', category)
    context = { 
        'category': category,
        'products': products,
        'last5': last5,
    }
    return dmp_render(request, 'searchresults.html', context)