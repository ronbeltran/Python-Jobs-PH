
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout

#from social_auth.views import disconnect as social_auth_disconnect
from jobs.models import Entry


def home_page(request):
    posts = Entry.live.all()[0:20]
    variables = {
        'posts': posts,
    } 

    return render_to_response(
        'home.html', variables, context_instance=RequestContext(request),
    )    


def logout_page(request):
#    social_auth_disconnect(google,)
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required
def profile_redirect(request):
    return HttpResponseRedirect(reverse('profiles_profile_detail', kwargs = {'username':request.user,}))


