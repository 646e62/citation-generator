from django.contrib import admin

# Register your models here.

from .models import Citation
from .models import Submission
from .models import Changelog

admin.site.register(Citation)
admin.site.register(Submission)
admin.site.register(Changelog)

