from django.shortcuts import render


# home page
def index(request):
    """View for home page of the project."""
    return render(request, 'index.html')