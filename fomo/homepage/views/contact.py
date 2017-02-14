from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):
    print('>>>>>>>>>>>>>>>>>> in process qeust')
    #user comes here twice
    #time 1: a GET request for the empty form
    #time 2: a POST request for the filled-in form
    if request.method =='POST':
        print('>>>>>>>>>>>>>>>>>> posted')
        form = ContactForm(request.POST)
        if form.is_valid():
            form_name = form.cleaned_data.get('name')
            print('>>>>>>>>>>>>>>>>>> valid')
            #act on the form here
            return HttpResponseRedirect('/homepage/contact')

    else:
        #prepare an empty form
        form = ContactForm()


    #render the template
    return dmp_render(request, 'contact.html', {
    'form':form,
    })


class ContactForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    message = forms.CharField(label='Message', max_length=1000)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        parts = name.strip().split()
        if len(parts) <= 1:
            raise forms.ValidationError('Please enter both first and last name')


        #return the name back to django
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')

        #return the email back to django
        return email

    def clean_message(self):
        message = self.cleaned_data.get('message')

        #return the message back to django
        return message
