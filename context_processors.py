
from django.conf import settings

def context_variables(request):
    return {
        'settings': settings,
        'show_abs_uri': request.build_absolute_uri(),
        'prefix_abs_uri': str(request.build_absolute_uri('/')).rstrip('/'),
    }   

