# ia_chat_pdf/views.py

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .query_data import query_rag
from .query_data import query_correct_response


@require_http_methods(["GET", "POST"])
def home(request):
    if request.method == 'POST':
        query_text = request.POST.get('query_text', '')
        correct_response = request.POST.get('correct_response', '')
        if correct_response != '':
            query_correct_response(correct_response, query_text)
            return render(request, 'index.html')

        if query_text:
            response_text = query_rag(query_text)
            data = {
                'query_text': query_text,
                'response_text': response_text,
            }
            return JsonResponse(data)
    return render(request, 'index.html')
        
