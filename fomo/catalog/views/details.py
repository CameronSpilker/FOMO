from django.conf import settings
from django_mako_plus import view_function
from catalog import models as cmod
from django.http import HttpResponse, HttpResponseRedirect


from .. import dmp_render, dmp_render_to_string

#details
@view_function
def process_request(request):
    pid = request.urlparams[0]

    try:
        product = cmod.Product.objects.get(id=pid)
    except cmod.Product.DoesNotExist:
        return HttpResponseRedirect('/catalog/index/')

    # add to the last 5 viewd items
    # request.last5.insert(0, product.id) -
    # request.last5.append(product.id)

    request.last5.insert(0, product.id)

    while len(request.last5) > 5:
        request.last5.pop()

    #request.last5 = request.last5[:5]

    #what if this item was already in the list


    return dmp_render(request, 'details.html', {})
