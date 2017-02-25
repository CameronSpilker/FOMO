from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django_mako_plus import view_function
from datetime import datetime
from account import models as amod
from formlib.form import FormMixIn
from django import forms
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.decorators import login_required, permission_required
from .. import dmp_render, dmp_render_to_string

@view_function
@login_required(login_url='/account/login/')
@permission_required('account.add_fomouser', login_url='/manager/permissions/')
def process_request(request):
    print(">>>>>>>in is request")

    form = CreateUserForm(request)
    if form.is_valid():
        print(">>>>>>>in is valid")
        form.commit()
        return HttpResponseRedirect('/manager/edituserstable/')


    context = {
        'form': form,

    }
    return dmp_render(request, 'createuser.html', context)

class CreateUserForm(FormMixIn, forms.Form):

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
        self.fields['set_password'] = forms.CharField(label="Password")
        self.fields['shipping_address'] = forms.CharField(label="Shipping Address", max_length=100)
        self.fields['billing_address'] = forms.CharField(label="Billing Address", max_length=100)
        self.fields['birthdate'] = forms.DateField(label="Birthdate")
        self.fields['credit_card'] = forms.CharField(label="Credit Card", max_length=20)
        self.fields['cc_exp_date'] = forms.DateField(label="Credit Card Expiration Date")
        self.fields['cc_code'] = forms.CharField(label="Credit Card CVS Code", max_length=4)

        self.fields['groups'] = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
        self.fields['permissions'] = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)


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
        fomouser.set_password(self.cleaned_data.get('set_password'))
        fomouser.shipping_address = self.cleaned_data.get('shipping_address')
        fomouser.billing_address = self.cleaned_data.get('billing_address')
        fomouser.birthdate = self.cleaned_data.get('birthdate')
        fomouser.credit_card = self.cleaned_data.get('credit_card')
        fomouser.cc_exp_date = self.cleaned_data.get('cc_exp_date')
        fomouser.cc_code = self.cleaned_data.get('cc_code')


        fomouser.save()
        fomouser.user_permissions.set(self.cleaned_data.get('permissions'))
        fomouser.groups.set(self.cleaned_data.get('groups'))
        fomouser.save()
