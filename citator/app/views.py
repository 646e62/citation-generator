from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse

from .models import Changelog, Citation
from .scripts.mcgill_jurisprudence_rules import generate_citation
from .scripts.api_calls import call_api_jurisprudence


def index(request):
    return render(request, 'app/index.html')


def changelog(request):
    changelog = Changelog.objects.all()
    return render(request, 'app/changelog.html', {'changelog': changelog})


def process_text(request):
    # Get the text
    if request.method == 'POST':
        url = request.POST['url']
        pinpoint = request.POST['pinpoint']
        
        # Check to see if the result is already in the database
        try:
            citation_data = Citation.objects.get(url=url)
            result = generate_citation(citation_data, pinpoint)
            return render(request, 'app/result.html', {'result': result})
     
        # Call the API if it is not
        except Citation.DoesNotExist:
            citation_data = call_api_jurisprudence(url)
            print(citation_data)
            if citation_data is None:
                return render(request, 'app/error.html')
            else:
                # Save the citation data to the database
                
                result = generate_citation(citation_data, pinpoint)
                return render(request, 'app/result.html', {'result': result})
    else:
        return render(request, 'app/index.html')

