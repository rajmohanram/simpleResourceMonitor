from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Endpoint


# /mweb/endpoints
@login_required()
def endpoints(request):
    """View for managing HTTP endpoint."""
    if request.method == 'GET':
        endpoints = Endpoint.objects.all()
        context = {"endpoints": endpoints}
        return render(request, 'monitorhttp/endpoints.html', context=context)
    if request.method == 'POST':
        if request.POST.get('id'):
            id = request.POST.get('id')
            name = request.POST.get('endpoint')
            url = request.POST.get('url')
            Endpoint.objects.filter(id=id).update(name=name, url=url)
        else:
            name = request.POST.get('endpoint')
            url = request.POST.get('url')
            Endpoint.objects.create(name=name, url=url)
        return redirect('monitorhttp.endpoints')


# /mweb/get-endpoint?id=10
def get_endpoint(request):
    """View to get an HTTP endpoint detail."""
    id = request.GET.get('id')
    endpoint = Endpoint.objects.values_list('id', 'name', 'url').get(id=id)
    return JsonResponse({"endpoint": endpoint})


# /mweb/get-endpoints
def get_endpoints(request):
    """View to get all HTTP endpoint detail."""
    endpoint = Endpoint.objects.values_list('id', 'name', 'url')
    endpoint_list = [i for i in endpoint]
    return JsonResponse({"endpoints": endpoint_list})


# /mweb/del-endpoint?id=10
@login_required()
def del_endpoint(request):
    """View for deleting an HTTP endpoint."""
    id = request.GET.get('id')
    Endpoint.objects.filter(id=id).delete()
    return redirect('monitorhttp.endpoints')


# /mweb/endpoints
@login_required()
def endpoints_status(request):
    """View for checking the status of all HTTP endpoint."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    context = {'client_ip': ip}
    return render(request, 'monitorhttp/endpoints-status.html', context=context)
