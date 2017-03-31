from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from account import models as amod
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

    # if product.id in request.last5:
    #     removeProduct = request.last5.index(product.id)
    #     del request.last5[removeProduct]
    # request.last5.insert(0, product.id)
    # # elif pid in request.last5:
    # #     request.last5


    # if len(request.last5) > 6:
    #     request.last5[:5]

    # products = cmod.Product.objects.filter(id__in=request.last5).exclude(id=product.id)


    last5Item = amod.ProductHistory()
    last5Item.fomouser = request.user
    last5Item.product = product
    last5Item.save()


    form = AddToCartForm(request, product=product, initial={
        'product_id': pid,
        'quantity': 1,
        })
    if form.is_valid():
        form.commit()

    context = {
        'category': category,
        # 'products': products,
        'product': product,
        'form': form,
    }
    return dmp_render(request, 'productdetails-ajax.html' if request.method == 'POST' else 'productdetails.html', context)

    # return dmp_render(request, 'productdetails.html', context)


class AddToCartForm(FormMixIn, forms.Form):
    form_id = 'cart_form'
    form_submit = 'Add to Cart'

    def init(self, product):
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(required=False, min_value=1, max_value=product.quantity)
            self.fields['product_id'] = forms.IntegerField(required=True, widget=forms.HiddenInput())
        else:
            self.fields['quantity'] = forms.IntegerField(required=False, widget=forms.HiddenInput())
            self.fields['product_id'] = forms.IntegerField(required=True, widget=forms.HiddenInput())


    def clean(self):
        quantity = self.cleaned_data.get('quantity')
        pid = self.cleaned_data.get('product_id')
        try:
            product = cmod.Product.objects.get(id=pid)
        except cmod.Product.DoesNotExist:
            raise forms.ValidationError("Product does not exist, try another one.")

        if hasattr(product, 'quantity'):
            count = product.quantity
        else:
            count = 1
        if quantity > count:
            raise forms.ValidationError("Try a lower quantity")
        return self.cleaned_data

    def commit(self):
        pid = self.cleaned_data.get('product_id')
        product = cmod.Product.objects.get(id=pid)
        cart = self.request.user.get_cart()
        qty_ordered = self.cleaned_data.get('quantity')

        try:
            item = amod.ShoppingItem.objects.get(product__id=product.id)
            item.qty_ordered += qty_ordered
            item.save()
        except amod.ShoppingItem.DoesNotExist:
            item = 'None'
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', item)
        print(cart)

        if item not in cart:
            #add to the cart
            si = amod.ShoppingItem()
            si.product = product
            si.fomouser = self.request.user
            if hasattr(product, 'quantity'):
                si.qty_ordered = self.cleaned_data.get('quantity')
            else:
                si.qty_ordered = 1
            si.save()
            #update product history
            ph = amod.ProductHistory()
            ph.product = product
            ph.fomouser = self.request.user
            ph.qty_ordered = self.cleaned_data.get('quantity')
            ph.added = True
            ph.in_cart = True
            ph.save()


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
