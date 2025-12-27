from django.shortcuts import render

# Create your views here.

def home_page(request):

	return render(request, 'index.html')


def api_page(request):

	return render(request, 'api.html')


def doc_page(request):

	return render(request, 'doc.html')