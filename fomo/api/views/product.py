from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from account import models as amod
from catalog import models as cmod
import json
from array import array
from django import forms
from django.contrib.postgres.search import SearchVector

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):
    products = []
    error = ''
    try:
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        pname = request.GET.get('pname')
        cat = request.GET.get('cat')

        qty = cmod.Product.objects.all()

        if min_price:
            try:
                qty = qty.filter(price__gte=min_price)
            except Exception:
                error = 'Please enter a valid number for min_price'
        if max_price:
            try:
                qty = qty.filter(price__lte=max_price)
            except Exception:
                error = 'Please enter a valid number for max_price'
        if pname:
            try:
                qty = qty.filter(name__icontains=pname)
            except Exception:
                error = 'Please enter an insturment name'
        if cat:
            try:
                qty = qty.filter(category__name__icontains=cat)
            except Exception:
                error = 'Please enter a category'

        if len(qty) != 0:

            for p in qty:
                if hasattr(p, 'quantity'):
                    data = {
                        'name': p.name,
                        'category': p.category.name,
                        'price': p.price,
                        'desc': p.desc,
                        'quantity': getattr(p, 'quantity', 0),
                    }
                    products.append(data)
                else:
                    data = {
                        'name': p.name,
                        'category': p.category.name,
                        'price': p.price,
                        'desc': p.desc,
                        'serial_number': getattr(p, 'serial_number', 0),
                    }
                    products.append(data)
        else:
            products = "No items were found"
        if error != '':
            products = error

    except cmod.Product.DoesNotExist:
        return JsonResponse('Sorry bad ID', safe=False)

    return JsonResponse(products, safe=False)


# test api
# r = request.get(url)
# results.append(r1.json())

# form = ProductForm(request.GET)
# print(form.cleaned_data.get('pname'))
# print(form.cleaned_data.get('min_price'))
# print(form.cleaned_data.get('max_price'))
# print(form.cleaned_data.get('desc'))
# print(form.cleaned_data.get('cat'))
# if not form.is_valid():
#     form.errors.as_json()
# else:
# HttpResponse(json.dumps({}), content_type="application/json")


# class ProductForm(forms.Form):

#     pname = forms.CharField()
#     min_price = forms.DecimalField()
#     max_price = forms.DecimalField()
#     desc = forms.CharField()
#     cat = forms.CharField()

#     def clean_pname(self):
#         pname = self.cleaned_data.get('name')

#         return pname

#     def clean_min_price(self):
#         min_price = self.cleaned_data.get('min_price')

#         return min_price

#     def clean_max_price(self):
#         max_price = self.cleaned_data.get('max_price')

#         return max_price

#     def clean_desc(self):
#         desc = self.cleaned_data.get('desc')

#         return desc

#     def clean_cat(self):
#         cat = self.cleaned_data.get('cat')

#         return cat

# data = {
#     'name': product.name,
#     'category': product.category,
#     'price': product.price,
#     'quantity': getattr(product, 'quantity', 0),
#     'serial_number': getattr(product, 'serial_number', 0),
#     }

# form = ProductForm(data)
# form.errors.as_json()

# min_price = request.GET.get('min_price')
# max_price = request.GET.get('max_price')

# qry = cmod.Product.objects
# if min_price:
#     qry = qry.filter(price__lte=min_price)
# if max_price:
#     qry = qry.filter(price__)

# # for p in qry:

# userSearch = request.urlparams[0]

# try:
#     product = cmod.Product.objects.annotate(search=SearchVector('desc') + SearchVector('name')).filter(search__icontains=userSearch)
# except amod.Product.DoesNotExist:
#     return HttpResponseNotFound('Bad product id')

# plist = []

# for p in product:

#     ret = {
#     'name': p.name,
#     'price': int(p.price),
#     'desc': p.desc,
#     'category': str(p.category),
#     }
#     plist.append(dict(ret))

# return JsonResponse(plist, safe=False)
# return HttpResponse(json.dumps(ret), content_type="application/json")
# postman is just a browser

# pname = cmod.Product.objects.filter(name__icontains=form.cleaned_data.get('pname'))
# min_price = cmod.Product.objects.filter(price__gte=form.cleaned_data.get('min_price'))
# max_price = cmod.Product.objects.filter(price__lte=form.cleaned_data.get('max_price'))
# desc = cmod.Product.objects.filter(desc=form.cleaned_data.get('desc'))
# cat = cmod.Category.objects.filter(name__icontains=form.cleaned_data.get('cat'))

# catpro = cmod.Product.objects.filter(category_id=cat.values_list('id', flat=True))
