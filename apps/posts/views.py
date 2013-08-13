from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from google.appengine.api import urlfetch

from posts.models import Entry, Category

def entry_detail(request, slug, year, month):
    entry = get_object_or_404(Entry, slug=slug, status=Entry.LIVE_STATUS)
    variables = RequestContext(request, {
        'entry':entry,
    }) 

    return render_to_response(
        'posts/entry_detail.html', variables,
    )    

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return object_list(request, queryset=category.live_entry_set(),
                       template_object_name='post', template_name='posts/entries_by_category.html',
                       extra_context={ 'category': category })

@login_required
def preview_list(request):
    drafts = Entry.objects.all().filter(status=Entry.DRAFT_STATUS)
    variables = RequestContext(request, {
        'posts':drafts,
    })

    return render_to_response(
        'posts/preview_list.html', variables,
    )

