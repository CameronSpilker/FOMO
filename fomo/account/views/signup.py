from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from django import forms
from .. import dmp_render, dmp_render_to_string

@view_function
def process_request(request):
    print(">>>>>>>in is request")

    form = SignUpPageForm(request)
    if form.is_valid():
        print(">>>>>>>in is valid")
        form.commit()
        return HttpResponseRedirect('/account/successsignup/')


    context = {
        'form': form,

    }
    return dmp_render(request, 'signup.html', context)

class SignUpPageForm(FormMixIn, forms.Form):

    def init(self):
        print(">>>>>>>in init")
        self.fields['first_name'] = forms.CharField(label="First Name", max_length=100)
        self.fields['last_name'] = forms.CharField(label="Last Name", max_length=100)
        self.fields['gender'] = forms.ChoiceField(label="Gender", choices=[
                    ['M', 'Male'],
                    ['F', 'Female'],
                    ['O', 'Other'],
                    ])
        self.fields['email'] = forms.EmailField(label="Email")
        self.fields['username'] = forms.CharField(label="Username", max_length=100)
        self.fields['password'] = forms.CharField(label="Password", widget=forms.PasswordInput())
        self.fields['shipping_address'] = forms.CharField(label="Shipping Address", max_length=100)
        self.fields['birthdate'] = forms.DateField(label="Birthdate")



    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = amod.FomoUser.objects.filter(username=username)
        if len(users) > 0:
            raise forms.ValidationError('Username taken, please choose another Username.')
        return username

    def commit(self):
        print(">>>>>>>in commit")

        fomouser = amod.FomoUser()

        fomouser.first_name = self.cleaned_data.get('first_name')
        fomouser.last_name = self.cleaned_data.get('last_name')
        fomouser.email = self.cleaned_data.get('email')
        fomouser.username = self.cleaned_data.get('username')
        fomouser.set_password(self.cleaned_data.get('password'))
        fomouser.shipping_address = self.cleaned_data.get('shipping_address')
        fomouser.birthdate = self.cleaned_data.get('birthdate')



        fomouser.save()
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        login(self.request, user)

