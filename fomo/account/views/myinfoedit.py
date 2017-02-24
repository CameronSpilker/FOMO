from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from formlib.form import FormMixIn
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
def process_request(request):
    print('>>>>>>>process request')

    try:
        print('>>>>>>>process request try')
        fomouser = amod.FomoUser.objects.get(id=request.urlparams[0])#.get is for a single product
        print('>>>', request.urlparams[0])
    except amod.FomoUser.DoesNotExist:
        print('>>>>>>>process request except')
        return HttpResponseRedirect('/account/myinfo/')

#create a form to edit the product information
#the inital data will be the product information
#if is_valid()
#   set form cleaned_data into the fields of product
#   product.save()

#process the form
    form = EditUserForm(request, fomouser=fomouser, initial={
        'first_name': fomouser.first_name,
        'last_name': fomouser.last_name,
        'username': fomouser.username,
        'email' : fomouser.email,
        'shipping_address': fomouser.shipping_address,
        'billing_address': fomouser.billing_address,
        'birthdate': fomouser.birthdate

    })
    if form.is_valid():
        print('>>>>>>>form is valid')
        form.commit(fomouser)
        return HttpResponseRedirect('/account/myinfo/')


    context = {
        'fomouser':fomouser,
        'form': form,
    }
    return dmp_render(request, 'myinfoedit.html', context)

class EditUserForm(FormMixIn, forms.Form):

    def init(self, fomouser):
        print('>>>>>>>init')
        self.fields['first_name'] = forms.CharField(label="First Name", max_length=100)
        self.fields['last_name'] = forms.CharField(label="Last Name", max_length=100)
        self.fields['email'] = forms.EmailField(label="Email")
        self.fields['username'] = forms.CharField(label="Username", max_length=100)
        self.fields['shipping_address'] = forms.CharField(label="Shipping Address", max_length=100)
        self.fields['billing_address'] = forms.CharField(label="Billing Address", max_length=100)
        self.fields['birthdate'] = forms.DateField(label="birthdate")
        self.fomouser = fomouser



    def clean_username(self):
        print('>>>>>>CLEAN')
        username = self.cleaned_data.get('username')
        users = amod.FomoUser.objects.filter(username=username).exclude(id=self.fomouser.id)
        if len(users) > 0:
            raise forms.ValidationError('Username taken, please choose another Username.')
        return username

    def commit(self, fomouser):
        print('>>>>>>>commit')
        fomouser.first_name = self.cleaned_data.get('first_name')
        fomouser.last_name = self.cleaned_data.get('last_name')
        fomouser.username = self.cleaned_data.get('username')
        fomouser.shipping_address = self.cleaned_data.get('shipping_address')
        fomouser.billing_address = self.cleaned_data.get('billing_address')
        fomouser.email = self.cleaned_data.get('email')
        fomouser.birthdate = self.cleaned_data.get('birthdate')

        fomouser.save()

    ###############DELETING OF product
@view_function
@login_required(login_url='/account/login/')
def delete(request):
    try:
        fomouser = amod.FomoUser.objects.get(id=request.urlparams[0])#.get is for a single product
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/account/myinfo/')

    fomouser.delete()
    return HttpResponseRedirect('/account/myinfo/')
