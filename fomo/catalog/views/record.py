from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from catalog import models as cmod
from account import models as amod
from django.contrib.auth.decorators import login_required, permission_required


import stripe

from .. import dmp_render, dmp_render_to_string


@view_function
@login_required(login_url='/account/login/')
def process_request(request):

    try:
        sale = amod.Sale.objects.get(id=request.urlparams[0])
    except (TypeError, amod.Sale.DoesNotExist):
        return HttpResponseRedirect('/catalog/index1/')

    saleitem = amod.SaleItem.objects.filter(sale__id=sale.id)
    payment = amod.Payment.objects.filter(sale__id=sale.id)


    return dmp_render(request, 'record.html', {
        'sale': sale,
        'saleitem': saleitem,
        'payment': payment,
    })


    # contact_message = "%s: %s via %s" % (
    #     form.cleaned_data.get('name'),
    #     form.cleaned_data.get('message'),
    #     form.cleaned_data.get('email')
    # )