from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from account import models as amod
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string
from django.contrib.postgres.search import SearchVector

@view_function
@login_required
def process_request(request):
    products = cmod.Product.objects.order_by().all()
    # picture = cmod.ProductPicture.objects.all()
    category = cmod.Category.objects.order_by('name')
    cart = request.user.get_cart()
    last5 = request.user.last5()

    context = {
        'cart': cart,
        'last5': last5,
        'products': products,
        'category': category,
    }

    return dmp_render(request, 'shoppingcart.html', context)



@view_function
def delete(request):
    try:
        shoppingitem = amod.ShoppingItem.objects.get(id=request.urlparams[0])
        # producthistory = amod.ProductHistory.objects.get(fomouser__id=request.user.id)
        #.get is for a single product
    except amod.ShoppingItem.DoesNotExist:
        return HttpResponseRedirect('/catalog/shoppingcart/')

    # producthistory.in_cart = False
    shoppingitem.delete()

    return HttpResponseRedirect('/catalog/shoppingcart/')

@view_function
def clear_cart(request):

    request.user.clear_cart()

    return HttpResponseRedirect('/catalog/shoppingcart/')
