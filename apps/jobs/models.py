import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from accounts.models import UserProfile

class Company(models.Model):
    name = models.CharField(max_length=100, help_text=_('Maximum 100 characters.'))
    slug = models.SlugField(help_text=_("Suggested value automatically generated from title. Must be unique."))
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    address = models.CharField(max_length=250, help_text=_('Company location or address. Maximum 100 characters.'))
    telephone = models.CharField(max_length=50, help_text=_('Company telephone or landline number. Maximum 50 characters.'))
    fax = models.CharField(max_length=50, blank=True, help_text=_('Company facsimile/fax number. Maximum 50 characters.'))
    email = models.EmailField(max_length=50, help_text=_('Company email address. Maximum 50 characters.'))
    url = models.URLField(max_length=250, blank=True, help_text=_('Company website url. Maximum 250 characters.'))
    description_html = models.TextField(help_text=_("An overview or a short description of your company.") )
    author = models.ForeignKey(User)

    class Meta:
        ordering = ['name']
        verbose_name_plural = _("Companies")

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('job_company_detail', (), {'object_id':self.id, 'slug':self.slug})

    get_absolute_url = models.permalink(get_absolute_url)

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.name)
        super(Company, self).save(force_insert, force_update)

#    def live_entry_set(self):
#        from jobs.models import Entry
#        return self.entry_set.filter(company=Entry.company)


class Category(models.Model):
    title = models.CharField(max_length=250,
        help_text=_('Maximum 50 characters.'))
    slug = models.SlugField(unique=True,
        help_text=_("Suggested value automatically generated from title. Must be unique."))
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    description_html = models.TextField(help_text=_("Short description"), blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('job_category_detail', (), {'slug':self.slug})

    get_absolute_url = models.permalink(get_absolute_url)

    def live_entry_set(self):
        from jobs.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)


class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=self.model.LIVE_STATUS)

class ExpiredEntryManager(models.Manager):
    def get_query_set(self):
        return super(ExpiredEntryManager, self).get_query_set().filter(status=self.model.EXPIRED_STATUS)

class DraftsEntryManager(models.Manager):
    def get_query_set(self):
        return super(DraftsEntryManager, self).get_query_set().filter(status=self.model.DRAFT_STATUS)


class Entry(models.Model):

    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    EXPIRED_STATUS = 3
    HIDDEN_STATUS = 4
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (EXPIRED_STATUS, 'Expired'),
        (HIDDEN_STATUS, 'Hidden'),
    )

    TWO_MONTHS = 1
    FOUR_MONTHS = 2
    SIX_MONTHS = 3
    VISIBILITY_CHOICES = (
        (TWO_MONTHS, 'Two Months'),
        (FOUR_MONTHS, 'Four Months'),
        (SIX_MONTHS, 'Six Months'),
    )

    FULL_TIME = 1
    PART_TIME = 2
    JOB_TYPE_CHOICES = (
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
    )

    LOCATION_CHOICES = (
        ('Home', (
                ('Home','Work from home'),
            )
        ),
        ('Philippines', (
                ('ARMM','Armm'),
                ('BICOL_REGION','Bicol Region'),
                ('CAR','C.A.R.'),
                ('CAGAYAN_VALLEY','Cagayan Valley'),
                ('CARAGA','Caraga'),
                ('CENTRAL_LUZON','Central Luzon'),
                ('CENTRAL_MINDANAO','Central Mindanao'),
                ('CENTRAL_VISAYAS','Central Visayas'),
                ('EASTERN_VISAYAS','Eastern Visayas'),
                ('ILOCOS_REGION','Ilocos Region'),
                ('NCR','National Capital Region'),
                ('NORTHERN_MINDANAO','Northern Mindanao'),
                ('SOUTHERN_MINDANAO','Southern Mindanao'),
                ('SOUTHERN_TAGALOG','Southern Tagalog'),
                ('WESTERN_MINDANAO','Western Mindanao'),
                ('WESTERN_VISAYAS','Western Visayas'),
            )
        ),
        ('Overseas', (
                ('BANGLADESH', 'Bangladesh'),
                ('CHINA', 'China'),
                ('HONG_KONG', 'Hong Kong'),
                ('INDIA', 'India'),
                ('INDONESIA', 'Indonesia'),
                ('JAPAN', 'Japan'),
                ('MALAYSIA', 'Malaysia'),
                ('SINGAPORE', 'Singapore'),
                ('THAILAND', 'Thailand'),
                ('VIETNAM', 'Vietnam'),
            )
        ),
        ('Other', (
                ('AFRICA', 'Africa'),
                ('ASIA_MIDDLE_EAST', 'Asia - Middle East'),
                ('ASIA_OTHERS', 'Asis - Others'),
                ('AUSTRALIA', 'Australia'),
                ('NEW_ZEALAND', 'New Zealand'),
                ('EUROPE', 'Europe'),
                ('NORTH_AMERICA', 'North America'),
                ('SOUTH_AMERICA', 'South America'),
            )
        ),
    )


    # Core fields.
    job_title = models.CharField(max_length=100, help_text=_("Maximum 100 characters."))
    slug = models.SlugField(max_length=100, help_text=_("Suggested value automatically generated from title."))
    body_html = models.TextField(help_text=_("Include here the job overview, description, qualifications..etc"))
    howto_apply_html = models.TextField(help_text=_("Instructions on how to apply.."))
    salary = models.CharField(max_length=100, blank=True, help_text=_("Salary, if confidential leave blank.") )
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default=LOCATION_CHOICES[0],
        help_text=_("By default we reserve the right to review the job posting before it is publicly displayed."))

    # Metadata.
    author = models.ForeignKey(User)
    has_expired = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS,
        help_text=_("By default we reserve the right to review the job posting before it it publicly displayed."))
#    type = models.IntegerField(choices=JOB_TYPE_CHOICES, default=FULL_TIME,
#        help_text=_("Specify job type."))
    visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=TWO_MONTHS,
        help_text=_("Specify how long the job will be available."))
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    # Categorization. Industry/Specialization
    categories = models.ForeignKey(Category)
    company_name = models.ForeignKey(Company)

    objects = models.Manager()
    live = LiveEntryManager()
    expired = ExpiredEntryManager()
    drafts = DraftsEntryManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = _("Job Entries")

    def __unicode__(self):
        return self.job_title

    def save(self, force_insert=False, force_update=False):
        self.slug = slugify(self.job_title)
        super(Entry, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return ('job_entry_detail', (), { 'slug': self.slug, 'object_id':self.id,  })

    get_absolute_url = models.permalink(get_absolute_url)

