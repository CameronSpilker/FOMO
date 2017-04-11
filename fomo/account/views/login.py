from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from account import models as amod
from ldap3 import Server, Connection, ALL

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
        'form': form,
        })

class LoginForm(FormMixIn, forms.Form):
    print('>>>>>>>>>>>>>>in the form')
    def init(self):
        print('>>>>>>>>>>>>>>in the init')
        self.fields['username'] = forms.CharField(required=True)
        self.fields['password'] = forms.CharField(required=True, widget=forms.PasswordInput())


def clean(self):
        userLocal = self.cleaned_data.get('username') + '@familyorientedmusic.local'
        userNet = self.cleaned_data.get('username') + '@familyorientedmusic.net'

        s = Server('128.187.61.57', port=389, use_ssl=False, get_info=ALL)
        c = Connection(s, user=userLocal, password=self.cleaned_data.get('password'), auto_bind='NONE', version=3, authentication='SIMPLE', client_strategy='SYNC', auto_referrals=True, check_names=True, read_only=False, lazy=False, raise_exceptions=False)
        if not c.bind():
            print('error in bind', c.user)
        else:
            currentuser = amod.FomoUser.objects.filter(username=self.cleaned_data.get('username'))
            print('after current user', currentuser)
            c.search('cn=users,dc=familyorientedmusic,dc=local','(objectclass=Person)',
                    attributes = ['mail', 'givenName', 'sn', 'streetaddress'])
            if not currentuser:
                for entry in c.response:
                    print('in the for loop', entry)
                    if 'mail' in entry['attributes']:
                        print('in the mail if statement', entry['attributes']['mail'])
                        if entry['attributes']['mail'] == userNet:
                            adFomoUser = amod.FomoUser()
                            adFomoUser.username = self.cleaned_data.get('username')
                            adFomoUser.set_password(self.cleaned_data.get('password'))
                            adFomoUser.first_name = entry['attributes']['givenName']
                            adFomoUser.last_name = entry['attributes']['sn']
                            adFomoUser.shipping_address = entry['attributes']['streetaddress']
                            adFomoUser.save()
                            user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
                            if user is None:
                                raise forms.ValidationError('Invalid username or password.')
                            return self.cleaned_data

            else:
                for entry in c.response:
                    print('in the for loop', entry)
                    if 'mail' in entry['attributes']:
                        print('in the mail if statement', entry['attributes']['mail'])
                        if entry['attributes']['mail'] == userNet:
                            currentuser[0].first_name = entry['attributes']['givenName']
                            currentuser[0].last_name = entry['attributes']['sn']
                            currentuser[0].shipping_address = entry['attributes']['streetaddress']
                            currentuser[0].save()
                            user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
                if user is None:
                    raise forms.ValidationError('Invalid username or password.')
                return self.cleaned_data


        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))

        if user is None:
            raise forms.ValidationError('Invalid username or password.')

        return self.cleaned_data




#login belongs inside of commit
def commit(self):
    user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
    login(self.request, user)



@view_function
def modal(request):
    print('>>>>>>>>>>>>>>in the request')
    form = ModalLoginForm(request)
    if form.is_valid():
        print('>>>>>>>>>>>>>>in the is valid')
        #do the form action
        form.commit()
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        return HttpResponse('''
            <script>
            window.location.href = '/account/successlogin/';
            </script>

            ''')
        # if request.GET.get('next') is not None:
        #     return HttpResponseRedirect('/homepage/index/')
        # else:
        #     return HttpResponseRedirect(request.GET.get('next')

    return dmp_render(request, 'login.modal.html', {
        'form': form,
        })

class ModalLoginForm(LoginForm):
    form_action = '/account/login.modal/'