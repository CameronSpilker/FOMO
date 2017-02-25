from django.conf import settings
from django.http import HttpResponseRedirect
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from django.contrib.auth.decorators import login_required, permission_required

from .. import dmp_render, dmp_render_to_string


@view_function
@login_required(login_url='/account/login/')
@permission_required('account.change_fomouser', login_url='/manager/permissions/')
def process_request(request):
    print('>>>>>>>>>>>>>>in the request')
    form = ChangePasswordForm(request)
    if form.is_valid():
        print('>>>>>>>>>>>>>>in the is valid')
        #do the form action
        form.commit()
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        return HttpResponseRedirect('/manager/edituserstable/')

    context = {
        'form': form,
    }

    return dmp_render(request, 'mchangepassword.html', context)

class ChangePasswordForm(FormMixIn, forms.Form):
    print('>>>>>>>>>>>>>>in the form')

    def init(self):
        print('>>>>>>>>>>>>>>in the init')
        self.fields['username'] = forms.CharField(required=True)
        self.fields['password'] = forms.CharField(required=True, widget=forms.PasswordInput())
        self.fields['passwordNEW'] = forms.CharField(label="New Password", required=True, widget=forms.PasswordInput())
        self.fields['passwordNEW2'] = forms.CharField(label="Confirm New Password", required=True, widget=forms.PasswordInput())


    # def clean_username(self):
        #un = self.cleaned_data.get('username')

        #return un

    #this is where you check all of the values
    def clean(self):
        print('>>>>>>>>>>>IN the clean')
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        passwordNEW = self.cleaned_data.get('passwordNEW')
        passwordNEW2 = self.cleaned_data.get('passwordNEW2')
        print(passwordNEW)
        print(passwordNEW2)
        print(user)
        if passwordNEW != passwordNEW2:
            print('>>>>>>>>> password')
            raise forms.ValidationError('New passwords does not match.')

        if user is None:
            raise forms.ValidationError('Invalid username or password.')


        return self.cleaned_data

    #
    #login belongs inside of commit
    def commit(self):
        print('>>>>>>>>>>>>>>in the commit')
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user.is_authenticated:
            user.set_password(self.cleaned_data.get('passwordNEW'))
            user.save()
        # user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        # login(self.request, user)
        # user = self.user
