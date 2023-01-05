from django.db import models

# Create your models here.

class Citation(models.Model):
    url = models.URLField(max_length=200)
    language = models.CharField(max_length=2)
    jurisdiction = models.CharField(max_length=2)
    court = models.CharField(max_length=10)
    canlii_citation = models.CharField(max_length=200)
    date = models.DateField()
    style_of_cause = models.CharField(max_length=200)
    docket_number = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    mcgill_citation = models.CharField(max_length=200)

    def __str__(self):
        return self.mcgill_citation

