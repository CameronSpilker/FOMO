from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from catalog import models as cmod
from formlib.form import FormMixIn
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
@permission_required('catalog.add_product', login_url='/manager/permissions/')
def process_request(request):
    print(">>>>>>>in is request")

    form = CreateProductForm(request)
    if form.is_valid():
        print(">>>>>>>in is valid")
        form.commit()
        return HttpResponseRedirect('/manager/products/')


    context = {
        'form': form,

    }
    return dmp_render(request, 'createproduct.html', context)

class CreateProductForm(FormMixIn, forms.Form):

    def init(self):
        print(">>>>>>>in init")
        self.fields['name'] = forms.CharField(label="Product Name", max_length=100)
        self.fields['producttype'] = forms.ChoiceField(label='Product Type', choices=[
                    ['bulk', 'Bulk Product'],
                    ['rental', 'Rental Product'],
                    ['unique', 'Unique Product'],
            ], initial='bulk')
        self.fields['category'] = forms.ModelChoiceField(label="Category",
        queryset=cmod.Category.objects.order_by('name').all())
        self.fields['price'] = forms.DecimalField(label="Price")

        #BULK product
        # if hasattr(product, 'quanity'):
        self.fields['quantity'] = forms.DecimalField(label="Quantity", required=False, widget=forms.TextInput(attrs={'class': 'producttype-bulk'}))
        self.fields['reorder_trigger'] = forms.IntegerField(label="Reorder Trigger", required=False, widget=forms.TextInput(attrs={'class': 'producttype-bulk'}))
        self.fields['reorder_quantity'] = forms.IntegerField(label="Reorder Quantity", required=False, widget=forms.TextInput(attrs={'class': 'producttype-bulk'}))

        #UNIQUE and rental  product
        self.fields['serial_number'] = forms.CharField(label="Serial Number", required=False, widget=forms.TextInput(attrs={'class': 'producttype-not'}))





    def commit(self):
        print(">>>>>>>in commit")
        producttype = self.cleaned_data.get('producttype')
        print('<<<<<<<<<<<<<<<<<<<<<', producttype)
        if producttype == 'bulk':
            product = cmod.BulkProduct()

        elif producttype == 'rental':
            product = cmod.RentalProduct()

        elif producttype == 'unique':
            product = cmod.UniqueProduct()

        product.name = self.cleaned_data.get('name')
        product.category = self.cleaned_data.get('category')
        product.price = self.cleaned_data.get('price')

        if hasattr(product, 'quantity'):
            product.reorder_quantity = self.cleaned_data.get('reorder_quantity')
            product.reorder_trigger = self.cleaned_data.get('reorder_trigger')
            product.quantity = self.cleaned_data.get('quantity')
        else:
            product.serial_number = self.cleaned_data.get('serial_number')

        product.save()
