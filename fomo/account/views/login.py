from django.conf import settings
from django.http import HttpResponseRedirect
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):
    print('>>>>>>>>>>>>>>in the request')
    form = LoginForm(request)
    if form.is_valid():
        print('>>>>>>>>>>>>>>in the is valid')
        #do the form action
        form.commit()
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        return HttpResponseRedirect('/account/successlogin/')
        # if request.GET.get('next') is not None:
        #     return HttpResponseRedirect('/homepage/index/')
        # else:
        #     return HttpResponseRedirect(request.GET.get('next')

    return dmp_render(request, 'login.html', {
        'form':form,
        })

class LoginForm(FormMixIn, forms.Form):
    print('>>>>>>>>>>>>>>in the form')
    def init(self):
        print('>>>>>>>>>>>>>>in the init')
        self.fields['username'] = forms.CharField(required=True)
        self.fields['password'] = forms.CharField(required=True, widget=forms.PasswordInput())


    # def clean_username(self):
        #un = self.cleaned_data.get('username')

        #return un

    #this is where you check all of the values
    def clean(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError('Invalid username or password.')

        return self.cleaned_data

    #
    #login belongs inside of commit
    def commit(self):
        print('>>>>>>>>>>>>>>in the commit')
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        login(self.request, user)

#self.request
        #
        # if user is not None:
        #     login(request, user)
        #     print('>>>>>>>>>>>>>>auth')
        #     return True
        #         #go to account page
        #     # return HttpResponseRedirect('/account/index/')
        #     # Redirect to a success page.
        # else:
        #         # Return an 'invalid login' error message.
        #     print('>>>>>>>>>>>>>>NOTTTTTT')
        #     return False

    # print('>>>>>>>>>>>>>> in print boya')
    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # #authenticate the user
    # # username = 'Cougar'
    # # password = '1234'
    # user = authenticate(username=username, password=password)
    # #log the user in
