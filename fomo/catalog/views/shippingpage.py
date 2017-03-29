import googlemaps
from django.conf import settings
from googlemaps import client
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django_mako_plus import view_function
from catalog import models as cmod
from account import models as amod
from django.contrib.auth import authenticate, login
from formlib.form import FormMixIn

from .. import dmp_render, dmp_render_to_string



@view_function
def process_request(request):
    # gmaps = googlemaps.Client(key='AIzaSyAy5uR2XX2y51goP4wXe3i4KWxm1pmT3Nc')

    # # Geocoding an address
    # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    # pid = request.urlparams[0]
    # currentuser = request.user
    # try:
    #     print(request.urlparams[0])
    #     category = cmod.Category.objects.order_by('name')#.get is for a single product
    #     product = cmod.Product.objects.get(id=pid)
    #     fomouser = amod.FomoUser.objects.get(id=currentuser.id)
    #     print('>>>>>>>>>>', category)
    #     print('>>>>>>>>>>', product)
    # except (TypeError, cmod.Category.DoesNotExist):
    #     return HttpResponseRedirect('/catalog/index1/')


    print('>>>>>>>>>>>>>>in the request')
    form = ShippingPageForm(request, initial={
        # 'shipping_address': request.POST('shipping_address'),

    })

    print('>>> Before Valid')
    if form.is_valid():
        form.cleaned_data['shipping_address']
        print('>>>>>>>>>>>>>>in the is valid')
        #do the form action
        form.commit()
        # username = form.cleaned_data.get('username')
        # password = form.cleaned_data.get('password')
        return HttpResponseRedirect('/catalog/index1/')
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
    def init(self):
        print('>>>>>>>>>>>>>>in the init')
        self.fields['shipping_address'] = forms.CharField(label="Shipping Address", max_length=100)
      # if address1 is not None:
        self.fields['check_box'] = forms.CharField(widget=forms.CheckboxInput(), required=False)
      # else:
      #   self.fomouser = fomouser


        # , widget=forms.HiddenInput()


    # def clean_username(self):
        #un = self.cleaned_data.get('username')

        #return un

    #this is where you check all of the values
    def clean_shipping_address(self):
        print('>>>>>>>>in the clean')
        gmaps = googlemaps.Client(key='AIzaSyAy5uR2XX2y51goP4wXe3i4KWxm1pmT3Nc')
        shipping_address = self.cleaned_data.get('shipping_address')
        google = gmaps.geocode(shipping_address)
        #ask googles gecoding api for corrected address
        googleaddress = google[0]['formatted_address']
        # print(shipping_address)
        # print('>>>>>>Before IF', googleaddress)
        self.data = self.data.copy()

        if shipping_address != googleaddress:
          self.data['shipping_address'] = googleaddress
          print('>>>>IN THE IF', self.cleaned_data['shipping_address'])
          raise forms.ValidationError("Check the box if the corrected address is okay.")
          #if different
          # self.cleaned_data['address1'] = google address 1
          # raise forms.ValidationError("is this okay?") "check box to verify the address"

        return shipping_address

    #
    #login belongs inside of commit
    def commit(self):
        print('>>>>>>>>>>>>>>in the commit', self.cleaned_data.get('shipping_address'))
        pass