from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Foodlist, Food
from usda.client import UsdaClient
from decouple import config
from .forms import newfoodForm,newlogForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import requests


API_KEY = config('API_KEY')
client = UsdaClient(API_KEY)

def users(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form2 = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/foodlog/index/')
            #return render(request, 'foodlog/index.html', user)
        elif form2.is_valid():
            form2.save()
            username = form2.cleaned_data.get('username')
            password = form2.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            print('You got here!You got here!You got here!You got here!You got here!You got here!You got here!!')
            return render(request, 'foodlog/index.html', user)
    else:
        form = UserCreationForm()
        form2 = AuthenticationForm()
    return render(request, 'foodlog/users.html', {'form': form, 'form2':form2})
def index(request):
    user = get_object_or_404(User, pk=1)#request.user.id)
    latest_foodlists = user.foodlist_set.all().order_by('-eat_date')
    if request.method == 'POST':
        form = newlogForm(request.POST)
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
def foodlist_delete(request, pk):    
    foodlist = get_object_or_404(Foodlist, pk=pk)  # Get your current 
    if request.method == 'POST':         # If method is POST,
        foodlist.delete()                     # delete
        return redirect('/foodlog/index/')             # Finally, redirect to the homepage.

    return render(request, 'foodlog/index.html', {'foodlist': foodlist})
def food_delete(request, foodlist_id,food_id):
    foodlist = get_object_or_404(Foodlist, pk=foodlist_id)    
    food = get_object_or_404(Food, pk=food_id)  # Get your current 

    if request.method == 'POST':         # If method is POST,
        food.delete()                     # delete the 

    return render(request, 'foodlog/detail.html', {'foodlist': foodlist})

