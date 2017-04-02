from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from catalog import models as cmod
from account import models as amod
from django.contrib.auth.decorators import login_required, permission_required

import stripe

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):

    currentuser = request.user
    try:
        fomouser = amod.FomoUser.objects.get(id=currentuser.id)
    except (TypeError, amod.FomoUser.DoesNotExist):
        return HttpResponseRedirect('/catalog/index1/')

    cart = request.user.get_cart()

    print('>>>>>>>>>>>>>>in the request')
    form = CheckoutForm(request, fomouser=fomouser, initial={
        'first_name': fomouser.first_name,
        'last_name': fomouser.last_name,
        'shipping_address': fomouser.shipping_address,

    })
    if form.is_valid():
        print('>>>>>>>>>>>>>>in the is valid')
        #do the form action
        form.commit(fomouser)
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        return HttpResponseRedirect('/catalog/index1/')
        # if request.GET.get('next') is not None:
        #     return HttpResponseRedirect('/homepage/index/')
        # else:
        #     return HttpResponseRedirect(request.GET.get('next')

    return dmp_render(request, 'checkout.html', {
        'form': form,
        'fomouser': fomouser,
        'cart': cart,
    })

class CheckoutForm(FormMixIn, forms.Form):
    print('>>>>>>>>>>>>>>in the form')
    form_id = 'checkout_form'
    def init(self, fomouser):
        print('>>>>>>>>>>>>>>in the init')
        self.fields['first_name'] = forms.CharField(label="First Name", max_length=100)
        self.fields['last_name'] = forms.CharField(label="Last Name", max_length=100)
        self.fields['shipping_address'] = forms.CharField(label="Shipping Address", max_length=100)
        self.fields['stripe_token'] = forms.CharField(required=True, widget=forms.HiddenInput())
        self.fomouser = fomouser


        # , widget=forms.HiddenInput()


    # def clean_username(self):
        #un = self.cleaned_data.get('username')

        #return un

    #this is where you check all of the values
    def clean(self):
        print('>>>>>>>>in the clean')
        stripe.api_key = "sk_test_6I3M56BwEphFD854SNkXSHRl"
        total = round(self.fomouser.calc_total(), 0) * 100
        ret = stripe.Charge.create(
        amount=total,
        currency="usd",
        source=self.cleaned_data.get('stripe_token'),
        # obtained with Stripe.js
        )
        print('>>>>>>>>>>>>>', ret)

        if ret is '':
            raise forms.ValidationError('Card invalid, please try again.')
        return self.cleaned_data

    #
    #login belongs inside of commit
    def commit(self, fomouser):
        print('>>>>>>>>>>>>>>in the commit', self.cleaned_data.get('stripe_token'))
        fomouser.record_sale(self.cleaned_data.get('stripe_token'))
        print(fomouser.record_sale(self.cleaned_data.get('stripe_token')))
        pass

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



#############MODAL##############################
