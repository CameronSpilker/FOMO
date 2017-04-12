from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn
from catalog import models as cmod
from account import models as amod
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives

import stripe

from .. import dmp_render, dmp_render_to_string

#checkoutpy
@view_function
@login_required(login_url='/account/login/')
def process_request(request):

    currentuser = request.user
    try:
        fomouser = amod.FomoUser.objects.get(id=currentuser.id)
    except (TypeError, amod.FomoUser.DoesNotExist):
        return HttpResponseRedirect('/catalog/index1/')

    cart = request.user.get_cart()

    if (fomouser.get_cart_count() < 1):
        return HttpResponseRedirect('/catalog/index1/')


    form = CheckoutForm(request, fomouser=fomouser, initial={
        'first_name': fomouser.first_name,
        'last_name': fomouser.last_name,
        'shipping_address': fomouser.shipping_address,

    })

    if form.is_valid():

        form.commit(fomouser)
        last_sale = amod.Sale.objects.filter(fomouser__id=currentuser.id).last()
        print('last sale', last_sale)

        try:
            sale = amod.Sale.objects.get(id=last_sale.id)
            print('sale id', sale.id)
            print('last sale id', last_sale.id)
        except (TypeError, amod.Sale.DoesNotExist):
            return HttpResponseRedirect('/catalog/index1/')

        saleitem = amod.SaleItem.objects.filter(sale__id=sale.id)
        payment = amod.Payment.objects.filter(sale__id=sale.id)

        subject = 'Your FOMO Order Confirmation'
        from_email = 'no-reply@familyorientedmusic.net'
        to_email = [request.user.email]
        print('user email', to_email)
        contact_message = "%s: %s via %s" % (
            'To',
            request.user.first_name,
            'no-reply@familyorientedmusic.net'
        )

    # send_mail(subject,contact_message,from_email,to_email,fail_silently=False)
        msg = EmailMultiAlternatives(
            subject, contact_message, from_email, to_email)
        html_message = dmp_render_to_string(request, 'email.html', {
            'sale': sale,
            'saleitem': saleitem,
            'payment': payment,})
        msg.attach_alternative(html_message, "text/html")
        msg.send()



        return HttpResponseRedirect('/catalog/record/' + str(last_sale.id))
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
    form_submit = 'Pay Now'
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
        stripe.api_key = settings.STRIPE_API_SECRET
        total = round(self.fomouser.calc_total(), 0) * 100
        ret = stripe.Charge.create(
        amount=total,
        currency="usd",
        source=self.cleaned_data.get('stripe_token'),
        #obtained with Stripe.js
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
        # cart = self.request.user.get_cart()

        # ph = amod.ProductHistory()
        # ph.product = cart.product
        # ph.fomouser = self.request.user
        # ph.purchased = True
        # ph.save()


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
