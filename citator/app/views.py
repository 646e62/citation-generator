from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import Http404
from django.http import HttpResponse

from .models import Changelog, Citation
from .scripts.mcgill_jurisprudence_rules import generate_citation, generate_pinpoint
from .scripts.api_calls import call_api_jurisprudence
from .scripts.database_functions import save_citation

def index(request):
    return render(request, 'app/index.html')


def changelog(request):
    changelog = Changelog.objects.all()
    return render(request, 'app/changelog.html', {'changelog': changelog})


def process_text(request):
    # Get the text
    if request.method == 'POST':
        url = request.POST['url']
        pinpoint_number = request.POST['pinpoint']
        pinpoint_type = request.POST['pinpoint_type']
        pinpoint_result = generate_pinpoint(pinpoint_number, pinpoint_type)

        # Check to see if the result is already in the database
        try:
            citation_model = Citation.objects.get(url=url)
            citation_data = model_to_dict(citation_model)
            result = generate_citation(citation_data, pinpoint_result)
            return render(request, 'app/result.html', {'result': result[1]})
     
        # Call the API if it is not
        except Citation.DoesNotExist:
            citation_data = call_api_jurisprudence(url)
            if citation_data is None:
                return render(request, 'app/error.html')
            else:
                # Save the citation data to the database
                result = generate_citation(citation_data, pinpoint_result)
                citation = save_citation(citation_data, url, result[0])
                return render(request, 'app/result.html', {'result': result[1]})

    else:
        return render(request, 'app/index.html')

