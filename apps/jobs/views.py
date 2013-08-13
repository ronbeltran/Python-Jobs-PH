import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_detail, object_list
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from jobs.models import Category, Entry, Company
from jobs.forms import EntryForm, CompanyForm

@login_required
def limited_object_detail(*args, **kwargs):
    return object_detail(*args, **kwargs)

@login_required
def limited_object_list(*args, **kwargs):
    return object_list(*args, **kwargs)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return object_list(request, queryset=category.live_entry_set(), 
                       extra_context={ 'category': category })

def index_redirect(request):
    return HttpResponseRedirect('/')

@login_required
def post_job(request):
    if request.method == 'POST':
        formset = EntryForm(request.POST, user=request.user)
        if formset.is_valid():
            formset.save(commit=False)
            formset.pub_date = datetime.datetime.now
            formset.save()
            return HttpResponseRedirect('/')
    else:
        formset = EntryForm(user=request.user)

    variables = RequestContext(request, {
        'formset': formset,
            })
    return render_to_response("jobs/post_entry.html", variables)

@login_required
def edit_job(request, object_id):
    entry = get_object_or_404(Entry,pk=object_id)
    if request.user.id != entry.author.id:
        return HttpResponseForbidden('<strong>Access Forbidden. You do not have permission to access this page. </strong>') # fix me 403 must be returned
    if request.method == 'POST':
        formset = EntryForm(instance=entry, data=request.POST, user=request.user)
        if formset.is_valid():
            entry.pk = object_id
            entry.save()
            if entry.status == Entry.DRAFT_STATUS:
               return HttpResponseRedirect(reverse('job_preview_detail', kwargs = {'object_id':entry.id,}))
            else:
               # if live or expired just display them
               return HttpResponseRedirect(reverse('job_entry_detail', kwargs = {'slug':entry.slug, 'object_id':entry.id,})) 
    else:
        formset = EntryForm(instance=entry, user=request.user)

    variables = RequestContext(request, {
        'formset': formset,
        'object_id': object_id,
            })
    return render_to_response("jobs/edit_job.html", variables)


@login_required
def edit_company(request, object_id):
    entry = get_object_or_404(Company,pk=object_id)
    if request.user.id != entry.author.id:
        return HttpResponseForbidden('<strong>Access Forbidden. You do not have permission to access this page. </strong>') #    if request.method == 'POST':
    if request.method == 'POST':
        formset = CompanyForm(instance=entry, data=request.POST, user=request.user)
        if formset.is_valid():
            entry.pk = object_id
            entry.save()
            return HttpResponseRedirect(reverse('job_company_detail', kwargs = {'slug':entry.slug, 'object_id':entry.id,}))
    else:      
        formset = CompanyForm(instance=entry, user=request.user)
        
    variables = RequestContext(request, {
        'formset': formset,
        'object_id': object_id,
            })

    return render_to_response("jobs/edit_company.html", variables)


@login_required
def post_company(request):
    if request.method == 'POST':
        formset = CompanyForm(request.POST, user=request.user)
        if formset.is_valid():
            formset.save(commit=False)
            formset.pub_date = datetime.datetime.now
            formset.save()
            return HttpResponseRedirect('/')
    else:
        formset = CompanyForm(user=request.user)

    variables = RequestContext(request, {
        'formset': formset,
            })
    return render_to_response("jobs/post_company.html", variables)

