def Last5ProductsMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('>>>>>>>> Beginning of middleware function')
        #.get is just to look into a dictonary
        request.last5 = request.session.get(
            'last5')  # [] is one way to do it

        # one way to do this
        #CRTL ALT  R fixes white spaces
        if request.last5 is None:
            request.last5 = []

        # Let Django continue the processing
        # Django will call your view function here
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        request.session['last5'] = request.last5[:6]
        print('!!!!!!!!!!!!! ending of middleware function ')
        return response

    return middleware
