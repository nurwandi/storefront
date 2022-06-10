from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

def profile(request):
    return render(request, 'profile.html', {'name' : 'Obi'})

def index(request):
    # quary_set = Product.objects.filter(title__icontains='coffee')
    # quary_set = Product.objects.filter(last_update__year=2021)
    quary_set = Product.objects.select_related('collection').all()
    return render(request, 'homepage.html', {'name' : 'Obi', 'products' : list(quary_set)})