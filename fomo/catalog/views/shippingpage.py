import googlemaps
from django.conf import settings
from googlemaps import client
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django_mako_plus import view_function
from catalog import models as cmod
from account import models as amod
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from formlib.form import FormMixIn

from .. import dmp_render, dmp_render_to_string


@view_function
@login_required(login_url='/account/login/')
def process_request(request):
    # gmaps = googlemaps.Client(key='AIzaSyAy5uR2XX2y51goP4wXe3i4KWxm1pmT3Nc')

    # # Geocoding an address
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    currentuser = request.user
    try:
        fomouser = amod.FomoUser.objects.get(id=currentuser.id)
    except (TypeError, amod.FomoUser.DoesNotExist):
        return HttpResponseRedirect('/catalog/index/')

    if (fomouser.get_cart_count() < 1):
        return HttpResponseRedirect('/catalog/index/')


    print('>>>>>>>>>>>>>>in the request')
    form = ShippingPageForm(request, fomouser=fomouser, initial={
        'shipping_address': fomouser.shipping_address,

    })

    print('>>> Before Valid')
    if form.is_valid():
        form.cleaned_data['shipping_address']
        print('>>>>>>>>>>>>>>in the is valid')
        #do the form action
        form.commit(fomouser)
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        return HttpResponseRedirect('/catalog/checkout/')
        # if request.GET.get('next') is not None:
        #     return HttpResponseRedirect('/homepage/index/')
        # else:
        #     return HttpResponseRedirect(request.GET.get('next')
    # print(form.data['shipping_address'])
    return dmp_render(request, 'shippingpage.html', {
        'form': form,
        # 'fomouser': fomouser,
    })

class ShippingPageForm(FormMixIn, forms.Form):
    print('>>>>>>>>>>>>>>in the form')
    form_id = 'shippingpage_form'
    form_submit = 'Continue'
    def init(self, fomouser):
        print('>>>>>>>>>>>>>>in the init')
        self.fields['shipping_address'] = forms.CharField(label="Shipping Address", max_length=100)
        # if count > 1:
        self.fields['check_box'] = forms.CharField(widget=forms.CheckboxInput(), required=False)
        # else:
        # self.fields['check_box'] = forms.CharField(widget=forms.HiddenInput(), required=False)
        self.fomouser = fomouser

    #this is where you check all of the values
    def clean_shipping_address(self):
        print('>>>>>>>>in the clean')
        gmaps = googlemaps.Client(key=settings.GOOGLE_SERVER_KEY)
        shipping_address = self.cleaned_data.get('shipping_address')
        google = gmaps.geocode(shipping_address)
        #ask googles gecoding api for corrected address
        print(google)
        googleaddress = google[0]['formatted_address']
        # print(shipping_address)
        # print('>>>>>>Before IF', googleaddress)
        self.data = self.data.copy()

        if shipping_address != googleaddress:
          self.data['shipping_address'] = googleaddress
          print('>>>>IN THE IF', self.cleaned_data['shipping_address'])
          raise forms.ValidationError("Select continue if the corrected address is okay.")
          #if different
          # self.cleaned_data['address1'] = google address 1
          # raise forms.ValidationError("is this okay?") "check box to verify the address"

        return shipping_address

    #
    #login belongs inside of commit
    def commit(self, fomouser):
        print('>>>>>>>>>>>>>>in the commit', self.cleaned_data.get('shipping_address'))
        fomouser.shipping_address = self.cleaned_data.get('shipping_address')
        fomouser.save()
