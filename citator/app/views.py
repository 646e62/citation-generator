from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .models import Changelog
from .scripts.mcgill_jurisprudence_rules import *
from .scripts.api_calls import *

def index(request):
    return render(request, 'app/index.html')


def changelog(request):
    changelog = Changelog.objects.all()
    return render(request, 'app/changelog.html', {'changelog': changelog})


def process_text(request):
    # Get the text
    if request.method == 'POST':
        text = str(request.POST.get('text_field'))
        result = generate_citation(text)
        return render(request, 'app/result.html', {'result': result})
    else:
        return render(request, 'app/index.html')

