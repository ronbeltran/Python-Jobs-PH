
from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed

from jobs.models import Entry, Company, Category
current_site = Site.objects.get_current()

class LatestJobsFeed(Feed):
    title = 'Latest Jobs for %s' % current_site
    link = '/feed/jobs/'
    description = 'Latest Jobs Posted'

    def items(self):
        return Entry.live.all()[:20]

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        return item.job_title

    def item_description(self, item):
        return item.body_html

    def item_guid(self, item):
        return "GUID:%s,%s:%s" % (current_site.domain,
            item.pub_date.strftime('%Y-%m-%d'),
            item.get_absolute_url())

class LatestCompaniesFeed(Feed):
    title = 'Latest Companies for %s' % current_site
    link = '/feed/companies/'
    description = 'Latest Companies Posted'

    def items(self):
        return Company.objects.all()[:20]

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description_html

    def item_guid(self, item):
        return "GUID:%s,%s:%s" % (current_site.domain,
            item.pub_date.strftime('%Y-%m-%d'),
            item.get_absolute_url())
