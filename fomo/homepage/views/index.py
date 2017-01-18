from django.conf import settings
from django_mako_plus import view_function
from django_mako_plus.template import get_template_loader
from datetime import datetime

@view_function
def process_request(request):
    context = {
        'now': datetime.now(),
    }

    # this syntax is only needed if you need to customize the way template rendering works
    tlookup = get_template_loader('/app/path/', subdir="my_templates")
    template = tlookup.get_template('index.html')
    return template.render_to_response(request=request, context=context)
