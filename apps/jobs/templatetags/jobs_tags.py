
from django.db.models import get_model
from django import template

from jobs.models import Entry

# get latest content for an object
def do_latest_content(parser, token):
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'get_latest_content'tag takes exactly four arguments")
    model_args = bits[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to 'get_latest_content' must be an 'application name'.'model name' string")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid model: %s" % bits[1])
    return LatestContentNode(model, bits[2], bits[4])


class LatestContentNode(template.Node):
    def __init__(self, model, num, varname):
        self.model = model
        self.num = int(num)
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''


# template tag for Archive Year in Sidebar 
def show_archive(parser, token):
    return ShowArchiveNode()

class ShowArchiveNode(template.Node):
    """this returns a list [2010, 2009, 2008, ..]"""
    def render(self, context):
        data = Entry.objects.all().filter(status=Entry.LIVE_STATUS)
        # this returns a list [2010, 2009, 2008, ..]
        year = ([d.year for d in data.dates('pub_date', 'year', order='DESC')])
        context['archive_year'] = year
        return ''


class CategoryEntriesCountNode(template.Node):
    def __init__(self, category):
        self.category = template.Variable(category)

    def render(self, context):
        try:
            category = self.category.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        count = Entry.live.filter(categories__exact=category).count()
        context['count'] = count
        return ''

def get_category_entries_count(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError, "%s tag requires exactly one argument" % token.contents.split()[0]
    return CategoryEntriesCountNode(bits[1] )    

def get_location(location):
    for key,value in Entry.LOCATION_CHOICES:
        for k,v in value:
            if k==location:
                return str(v)
    return  ''

def split(str,splitter):
    return str.split(splitter)[0]

def getstatus(str):
    stat = ''
    if int(str) == 1:
        stat = 'Live'
    elif int(str) == 2:
        stat = 'Draft'
    else:
        stat = 'Expired'
    return stat

register = template.Library()
register.filter('get_location', get_location)
register.filter('getstatus', getstatus)
register.filter('split', split)
register.tag('get_latest_content', do_latest_content)
register.tag('show_archive', show_archive)
register.tag('get_category_entries_count', get_category_entries_count)

