from django.contrib.sitemaps import Sitemap
from jobs.models import Entry, Category,Company 

class EntrySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Entry.live.all()

    def lastmod(self, obj):
        return obj.pub_date


class CategorySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.pub_date


class CompanySitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Company.objects.all()

    def lastmod(self, obj):
        return ''
