from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Foodlist, Food, SearchedFood
from usda.client import UsdaClient
from decouple import config
from .forms import newfoodForm,newlogForm,searchdatabaseForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import requests


API_KEY = config('API_KEY')
client = UsdaClient(API_KEY)

#Log in/Create A User
def users(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        form2 = AuthenticationForm(request.POST)
        nextForm = newlogForm()
        if 'signup' in request.POST:
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            #return redirect('/foodlog/index/')
        if user is not None:
            latest_foodlists = user.foodlist_set.all().order_by('-eat_date')
            login(request, user)
            context = {
                'form': nextForm, 'latest_foodlists': latest_foodlists
            }
            return render(request, 'foodlog/index.html', context)
    else:
        form = UserCreationForm()
        form2 = AuthenticationForm()
    return render(request, 'foodlog/users.html', {'form': form, 'form2':form2})

#User's list of logs
def index(request):
    user = get_object_or_404(User, pk=request.user.id)
    latest_foodlists = user.foodlist_set.all().order_by('-eat_date')
    totalCalories = []
    for foodlist in latest_foodlists:
        total = 0
        for foods in foodlist.food_set.all():
            total+=foods.calories
        totalCalories.append(total)

    latest_foodlists = zip(latest_foodlists, totalCalories)
    if request.method == 'POST':
        if 'add' in request.POST:
            form = newlogForm
            q = Foodlist(user = user)
            q.save()
        else:
            form = newlogForm(request.POST)
            if form.is_valid():
                q = Foodlist(eat_date=form.cleaned_data['newLog'], user = user)
                q.save()
    else:
        form = newlogForm()

    context = {
        'latest_foodlists': latest_foodlists, 'form': form
    }

    return render(request, 'foodlog/index.html', context)

#List of log's food
def detail(request, foodlist_id):
    foodlist = get_object_or_404(Foodlist, pk=foodlist_id)
    foods = []
    foodResults = []    
    if request.method == 'POST':
        if 'insert' in request.POST:
            form = newfoodForm(request.POST)
            form2 = searchdatabaseForm()
            if form.is_valid():
                foodlist.food_set.create(food_text=form.cleaned_data['newFood'], calories=form.cleaned_data['newCalories'])
                foodlist.save()
                print(request.POST)
        elif 'search' in request.POST:
            form = newfoodForm()
            form2 = searchdatabaseForm(request.POST)
            if form2.is_valid():
                searchtext = form2.cleaned_data['databaseSearch']
                foods_search = client.search_foods(searchtext, 1500)
                for x in range(1500):
                    try:
                        foods.append(next(foods_search))
                    except:
                        break
                for x in range(len(foods)):
                    report = client.get_food_report(foods[x].id)
                    for nutrient in report.nutrients:
                        if nutrient.name == 'Energy':
                            foodResults.append(SearchedFood(food_text=foods[x].name, calories=nutrient.value))
                            break
                            
        elif '+' in request.POST.values():            
            form = newfoodForm()
            form2 = searchdatabaseForm()
            pair = [key for key in request.POST.keys()][1].split("|")
            print(pair)
            foodlist.food_set.create(food_text=pair[0], calories=int(float(pair[1])))
            foodlist.save()
        else:
            form = newfoodForm()
            form2 = searchdatabaseForm()
            print(request.POST)
    else:
        form = newfoodForm()
        form2 = searchdatabaseForm()
    return render(request, 'foodlog/detail.html', {'foodlist': foodlist, 'form': form, 'form2': form2, 'foodResults': foodResults})

#Delete a foodlist
def foodlist_delete(request, pk):    
    foodlist = get_object_or_404(Foodlist, pk=pk)
    if request.method == 'POST':
        foodlist.delete()                  
        return redirect('/foodlog/index/')             

    return render(request, 'foodlog/index.html', {'foodlist': foodlist})

#Delete a food
def food_delete(request, foodlist_id,food_id):
    foodlist = get_object_or_404(Foodlist, pk=foodlist_id)    
    food = get_object_or_404(Food, pk=food_id)  

    if request.method == 'POST':         
        food.delete()                      

    return render(request, 'foodlog/detail.html', {'foodlist': foodlist})

