from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from formlib.form import FormMixIn
from django import forms
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    print('>>>>>>>process request')
    try:
        print('>>>>>>>process request try')
        fomouser = amod.FomoUser.objects.get(id=request.urlparams[0])#.get is for a single product
    except amod.FomoUser.DoesNotExist:
        print('>>>>>>>process request except')
        return HttpResponseRedirect('/manager/edituserstable/')

#create a form to edit the product information
#the inital data will be the product information
#if is_valid()
#   set form cleaned_data into the fields of product
#   product.save()

#process the form
    form = FomoUserEditForm(request, fomouser=fomouser, initial={
        'firstname': fomouser.first_name,
        'lastname': fomouser.last_name,
        'username': fomouser.username,
        'password': fomouser.password,
        'email': fomouser.email,
    })
    if form.is_valid():
        print('>>>>>>>form is valid')
        form.commit(fomouser)
        return HttpResponseRedirect('/manager/edituserstable/')


    context = {
        'fomouser':fomouser,
        'form': form,
    }
    return dmp_render(request, 'editusers.html', context)

class FomoUserEditForm(FormMixIn, forms.Form):

    def init(self, fomouser):
        print('>>>>>>>init')
        self.fields['firstname'] = forms.CharField(label="First Name", max_length=100)
        self.fields['lastname'] = forms.CharField(label="Last Name", max_length=100)
        self.fields['username'] = forms.CharField(label="Username", max_length=100)
        self.fields['password'] = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput())
        self.fields['email'] = forms.EmailField(label="Email", max_length=100)

    def commit(self, fomouser):
        print('>>>>>>>commit')
        fomouser.first_name = self.cleaned_data.get('firstname')
        fomouser.last_name = self.cleaned_data.get('lastname')
        fomouser.username = self.cleaned_data.get('username')
        fomouser.password = self.cleaned_data.get('password')
        fomouser.email = self.cleaned_data.get('email')

        fomouser.save()

    ###############DELETING OF product
@view_function
def delete(request):
    try:
        fomouser = amod.FomoUser.objects.get(id=request.urlparams[0])#.get is for a single product
    except amod.FomoUser.DoesNotExist:
        return HttpResponseRedirect('/manager/edituserstable/')

    fomouser.delete()
    return HttpResponseRedirect('/manager/edituserstable/')
