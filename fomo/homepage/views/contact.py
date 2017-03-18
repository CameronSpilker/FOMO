from django.conf import settings
from django import forms
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from formlib.form import FormMixIn
from django.contrib.auth.decorators import login_required, permission_required

from .. import dmp_render, dmp_render_to_string


@view_function
# # #you are suppose to add this permission to the group
# @permission_required('account.contactus', raise_exception=True)#account.contactus is an example
def process_request(request):
    # print('>>>>>>>>>>>>>>>>>> in process qeust')
    # #user comes here twice
    # #time 1: a GET request for the empty form
    # #time 2: a POST request for the filled-in form
    # if request.method =='POST':
    #     print('>>>>>>>>>>>>>>>>>> posted')
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         form_name = form.cleaned_data.get('name')
    #         print('>>>>>>>>>>>>>>>>>> valid')
    #         #act on the form here
    #         return HttpResponseRedirect('/homepage/contact')
    #
    # else:
    #     #prepare an empty form
    #     form = ContactForm()
    #
    #
    # #render the template
    form = ContactForm(request)
    if form.is_valid():
        form.commit()
        # email = form.cleaned_data.get('email')
        #send mail
        return HttpResponseRedirect('/homepage/successcontact/')



    return dmp_render(request, 'contact.html', {
    'form': form,
    })


class ContactForm(FormMixIn, forms.Form):

    SUBJECT_CHOICES = [

        ['payment', 'Payment issue'],
        ['upset', 'I am upset at something'],
        ['technical', 'I have a technical issue'],
        ['login', "I can't login"],
    ]

    def init(self):
        self.fields['name'] = forms.CharField(label='Full Name', max_length=100)
        self.fields['contacttype'] = forms.ChoiceField(label='Contact Type', choices=[
                ['phone', 'Phone Number'],
                ['email', 'Email Address'],
        ], initial='phone')
        self.fields['email'] = forms.EmailField(label='Email', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'contacttype-email'}))
        self.fields['phone'] = forms.CharField(label='Phone', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'contacttype-phone'}))
        self.fields['cell'] = forms.CharField(label='Cell', required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'contacttype-phone'}))
        self.fields['subject'] = forms.ChoiceField(label='Subject', choices=ContactForm.SUBJECT_CHOICES)
        self.fields['message'] = forms.CharField(label='Message', max_length=1000, widget=forms.Textarea())


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


    def commit(self):
        email = self.cleaned_data.get('email')
        #if self.request.user.is_superuser:
        #do some specific logic
