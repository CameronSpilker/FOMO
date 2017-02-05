from django.conf import settings
from django.http import HttpResponseRedirect
from django_mako_plus import view_function
from django.contrib.auth import authenticate, login

from .. import dmp_render, dmp_render_to_string


@view_function
def process_request(request):
    # username = request.POST['username']
    # password = request.POST['password']

    #authenticate the user
    username = 'Cougar'
    password = '1234'
    user = authenticate(username=username, password=password)
    #log the user in
    if user is not None:
        login(request, user)
        #go to account page
        return HttpResponseRedirect('/account/index/')
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect('/')
        ...
