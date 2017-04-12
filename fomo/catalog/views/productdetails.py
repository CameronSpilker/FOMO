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
        return HttpResponseRedirect('/catalog/index/')

    try:
        product_history = amod.ProductHistory.objects.filter(fomouser__id=request.user.id).filter(product__id=product.id).order_by('-id')
        #update product history
        print(product_history)
    except amod.ProductHistory.DoesNotExist:
        ph = amod.ProductHistory()
        ph.product = product
        ph.fomouser = request.user
        ph.save()

    cart = 0
    if request.user.is_authenticated:
        cart = request.user.get_cart().filter(product__id=product.id)
        for c in cart:
            print('>>>>>>>', c.id)
            print('>>>>>>>', c.product.name)
        print(">>>>>>>>>>> user cart", cart)

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
        'cart': cart,
    }
    return dmp_render(request, 'productdetails-ajax.html' if request.method == 'POST' else 'productdetails.html', context)

    # return dmp_render(request, 'productdetails.html', context)


class AddToCartForm(FormMixIn, forms.Form):
    form_id = 'cart_form'
    form_submit = 'Add to Cart'
    # form_action = '/catalog/productdetails/ ' + str(product.id)

    def init(self, product):
        if hasattr(product, 'quantity'):
            self.fields['quantity'] = forms.IntegerField(required=False, min_value=1, max_value=product.quantity)
            self.fields['product_id'] = forms.IntegerField(required=True, widget=forms.HiddenInput())
        else:
            self.fields['quantity'] = forms.IntegerField(required=False, widget=forms.HiddenInput())
            self.fields['product_id'] = forms.IntegerField(required=True, widget=forms.HiddenInput())


    def clean(self):
        present_quantity_ordered = self.cleaned_data.get('quantity')
        pid = self.cleaned_data.get('product_id')
        try:
            product = cmod.Product.objects.get(id=pid)
        except cmod.Product.DoesNotExist:
            raise forms.ValidationError("Product does not exist, try another one.")

        if hasattr(product, 'quantity'):
            quantity_available = product.quantity
        else:
            quantity_available = 1

        try:
            past_item_ordered = amod.ShoppingItem.objects.filter(fomouser__id=self.request.user.id).get(product__id=product.id)
            past_quantity_ordered = past_item_ordered.qty_ordered
        except amod.ShoppingItem.DoesNotExist:
            past_quantity_ordered = 0

        total_quantity_ordered = past_quantity_ordered + present_quantity_ordered
        print('total quantity ordered: ', total_quantity_ordered)
        print('quantity available: ', quantity_available)

        if total_quantity_ordered > quantity_available:
            print('print in if statment')
            raise forms.ValidationError("You cannot add more product to your cart than is available.")
            print('print in if statment (after)')

        return self.cleaned_data


    def commit(self):
        pid = self.cleaned_data.get('product_id')
        product = cmod.Product.objects.get(id=pid)
        cart = self.request.user.get_cart()
        qty_ordered = self.cleaned_data.get('quantity')

        try:
            item = amod.ShoppingItem.objects.filter(fomouser__id=self.request.user.id).get(product__id=product.id)
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
        try:
            product_history = amod.ProductHistory.objects.filter(fomouser__id=self.request.user.id).filter(product__id=product.id).order_by('-id')[0]
            #update product history
            print(product_history)
            product_history.added = True
            product_history.save()
        except amod.ProductHistory.DoesNotExist:
            raise forms.ValidationError('Product History Does not Exist')

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
