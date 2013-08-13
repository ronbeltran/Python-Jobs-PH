
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    title = models.CharField(max_length=250,
        help_text=_('Maximum 250 characters.'))
    slug = models.SlugField(unique=True,
        help_text=_("Suggested value automatically generated from title. Must be unique."))
    pub_date = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(User)
    description = models.TextField(help_text=_("Short description"), blank=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('category_detail', (), {'slug':self.slug})

    get_absolute_url = models.permalink(get_absolute_url)

    def live_entry_set(self):
        from posts.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)


class PublicLinkManager(models.Manager):
    def get_query_set(self):
        return super(PublicLinkManager, self).get_query_set().filter(status=self.model.PUBLIC_STATUS)

class PrivateLinkManager(models.Manager):
    def get_query_set(self):
        return super(PrivateLinkManager, self).get_query_set().filter(status=self.model.PRIVATE_STATUS)

class Link(models.Model):
    PUBLIC_STATUS = 1
    PRIVATE_STATUS = 2
    STATUS_CHOICES = (
        (PUBLIC_STATUS, 'Public'),
        (PRIVATE_STATUS, 'Private'),
    )

    title = models.CharField(max_length=250, help_text=_("Maximum 250 characters."))
    url = models.URLField(verify_exists=False, max_length=250, help_text=_("Maximum 250 characters."))
    description = models.TextField(help_text=_("Description."))
    author = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PUBLIC_STATUS,
        help_text=_("Only entries with public status will be publicly displayed."))

    public = PublicLinkManager()
    private = PrivateLinkManager()
    objects = models.Manager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = _("Links")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '%s' % (self.url, )


class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)


class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    # Core fields.
    title = models.CharField(max_length=250, help_text=_("Maximum 250 characters."))
    slug = models.SlugField(max_length=250,
        help_text=_("Suggested value automatically generated from title. Must be unique for the publication date."))

    # SEO 
    meta_description = models.TextField(help_text=_("Meta Description. Good for SEO."))
    meta_keywords = models.CharField(max_length=250, help_text=_("Meta Keywords. Separate with comma. Good for SEO.") )

    body_html = models.TextField(editable=True, blank=True)

    # Metadata.
    author = models.ForeignKey(User,related_name="%(app_label)s_%(class)s_related")
    enable_comments = models.BooleanField(default=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS,
        help_text=_("Only entries with live status will be publicly displayed."))
    pub_date = models.DateTimeField(default=datetime.now)

    # Categorization
    category = models.ForeignKey(Category)

    objects = models.Manager()
    live = LiveEntryManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = _("Blog Entries")

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        super(Entry, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return ('entry_detail', (), { 'year': self.pub_date.strftime('%Y'),
                                              'month': self.pub_date.strftime('%m'),
                                              #'day': self.pub_date.strftime('%d'),
                                              'slug': self.slug })


    get_absolute_url = models.permalink(get_absolute_url)

