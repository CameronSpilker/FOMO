from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string
from formlib.form import FormMixIn
from django import forms




@view_function
def process_request(request):   

    pid = request.urlparams[0]

    try:
        print(request.urlparams[0])
        category = cmod.Category.objects.order_by('name')  
        #.get is for a single product
        product = cmod.Product.objects.get(id=pid)
        print('>>>>>>>>>>', category)
        print('>>>>>>>>>>', product)
    except (TypeError, cmod.Category.DoesNotExist):
        return HttpResponseRedirect('/catalog/index1/')

    # if pid not in request.last5:
    #     request.last5.insert(0, product.id)

    if product.id in request.last5:
        removeProduct = request.last5.index(product.id)
        del request.last5[removeProduct]
    request.last5.insert(0, product.id)
    # elif pid in request.last5:
    #     request.last5


    if len(request.last5) > 6:
        request.last5[:5]

    products = cmod.Product.objects.filter(id__in=request.last5).exclude(id=product.id)

    form = AddToCartForm(request, product=product)
    if form.is_valid():
        form.commit()

    context = {
        'category': category,
        'products': products,
        'last5': request.last5,
        'product': product,
        'form': form,
    }
    return dmp_render(request, 'productdetails.html', context)


class AddToCartForm(FormMixIn, forms.Form):
    form_id = 'Cart'
    form_submit = 'Add to Cart'
    def init(self, product):
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(required=False, max_value=cmod.Product.objects.filter(id=product.id))

    def clean_quantity(self, product):
        qty = self.cleaned_data.get('quantity')
        count = product.quantity
        # if qty > count:
        #     raise forms.ValidationError("Try a lower quantity")
        return qty

    def commit(self):
        pass




@view_function
def modal(request):

    pid = request.urlparams[0]

    try:
        print(request.urlparams[0])
        picture = cmod.ProductPicture.objects.filter(product=pid)
        print(picture)
    except (TypeError, cmod.ProductPicture.DoesNotExist):
        return HttpResponseRedirect('/catalog/productdetails/pid')

    context = {
    'picture': picture,
    }

    return dmp_render(request, 'productdetails.modal.html', context)
