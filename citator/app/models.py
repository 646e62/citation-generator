from django.db import models
from django.utils import timezone

# Create your models here.

class Citation(models.Model):
    
    JURISDICTION_CHOICES = (
        ('ca', 'Canada'),
        ('bc', 'British Columbia'),
        ('ab', 'Alberta'),
        ('sk', 'Saskatchewan'),
        ('mb', 'Manitoba'),
        ('on', 'Ontario'),
        ('qc', 'Quebec'),
        ('nb', 'New Brunswick'),
        ('ns', 'Nova Scotia'),
        ('pe', 'Prince Edward Island'),
        ('nl', 'Newfoundland and Labrador'),
        ('nt', 'Northwest Territories'),
        ('nu', 'Nunavut'),
        )
    url = models.URLField(max_length=200)
    short_url = models.URLField(max_length=200)
    language = models.CharField(max_length=2)
    case_jurisdiction = models.CharField(
        max_length=2, 
        choices=JURISDICTION_CHOICES
        )
    court = models.CharField(max_length=10)
    canlii_citation = models.CharField(max_length=200)
    date = models.DateField()
    style_of_cause = models.CharField(max_length=200)
    docket_number = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)

    def __str__(self):
        return self.mcgill_citation

class Submission(models.Model):
    '''
    A database that tracks how often each time a CanLII URL is inputted. It
    stores the URL, the date, and the number of times it has been inputted, as
    well as the IP address of the user who inputted it. The IP address is used
    to determine which jurisdiction the request is coming from.
    '''
    url = models.URLField(max_length=200)
    date = models.DateField()
    times_inputted = models.IntegerField()
    ip_address = models.CharField(max_length=200)
    user_jurisdiction = models.CharField(max_length=2)

    def __str__(self):
        return self.url

class Changelog(models.Model):
    '''
    A database that tracks the changes made to the app. It stores the date, the
    version, and the changelog.
    '''
    date = models.DateTimeField(default=timezone.now)
    version = models.CharField(max_length=10)
    changelog = models.TextField()
    
    class Meta:
        verbose_name_plural = "changelogs"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return self.changelog

