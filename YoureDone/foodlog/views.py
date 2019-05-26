from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import Foodlist, Food
from usda.client import UsdaClient
from decouple import config
from .forms import newfoodForm,newlogForm
import requests

API_KEY = config('API_KEY')
client = UsdaClient(API_KEY)

def index(request):
    latest_foodlists = Foodlist.objects.order_by('-eat_date')[:7]
    if request.method == 'GET':
        form = newlogForm(request.GET)
        if form.is_valid():
            q = Foodlist(eat_date=form.cleaned_data['newLog'])
            q.save()
    else:
        form = newlogForm()

    context = {
        'latest_foodlists': latest_foodlists, 'form': form
    }

    return render(request, 'foodlog/index.html', context)
def detail(request, foodlist_id):
    foodlist = get_object_or_404(Foodlist, pk=foodlist_id)
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = newfoodForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            foodlist.food_set.create(food_text=form.cleaned_data['newFood'], calories=form.cleaned_data['newCalories'])
            foodlist.save()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = newfoodForm()

    return render(request, 'foodlog/detail.html', {'foodlist': foodlist, 'form': form})

def addFood(request, foodlist_id):
    foodlist = get_object_or_404(Foodlist, pk=foodlist_id)
    try:
        text = foodlist.food_set.get(pk=request.get['myFood'])
    except (KeyError, Food.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'foodlog/detail.html', {
            'foodlist': foodlist,
            'error_message': "You did not type anything.",
        })
    else:
        #foods_search = client.search_foods('text', 1)
        foodlist.food_set.create(food_text=text, calories=0)
        foodlist.food_set.save()
        return render(request, 'foodlog/detail.html', {'foodlist': foodlist})
def addfoodList(request):	
    latest_foodlists = Foodlist.objects.order_by('-eat_date')[:7]
    context = {
        'latest_foodlists': latest_foodlists,
    }
    return render(request, 'foodlog/index.html', context)