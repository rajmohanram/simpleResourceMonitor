from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# home page
# /
@login_required()
def home(request):
    """View for home page of the project."""
    return render(request, 'srmonitor/index.html')


# login page
# /login
def login(request):
    """View for login page of the project."""
    return render(request, 'srmonitor/login.html')



