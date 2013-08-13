
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from posts.models import Entry, Link, Category

current_site = Site.objects.get_current()

class LatestEntriesFeed(Feed):
    title = 'Latest blog entries for %s' % current_site.domain
    link = '/feeds/posts/'
    description = 'Latest blog entries posted.'

    def items(self):
        return Entry.live.all()[:10]

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body_html

    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain,
            item.pub_date.strftime('%Y-%m-%d'),
            item.get_absolute_url())


class LatestCategoriesFeed(Feed):
    title = 'Latest blog categories for %s' % current_site.domain
    link = '/feeds/categories/'
    description = 'Latest blog categories posted.'

    def items(self):
        return Category.objects.all()

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain,
            item.pub_date.strftime('%Y-%m-%d'),
            item.get_absolute_url())


class LatestLinksFeed(Feed):
    title = 'Latest blog links for %s' % current_site.domain
    link = '/feeds/links/'
    description = 'Latest blog links posted.'

    def items(self):
        return Link.public.all()

    def item_pubdate(self, item):
        return item.pub_date

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain,
            item.pub_date.strftime('%Y-%m-%d'),
            item.get_absolute_url())

