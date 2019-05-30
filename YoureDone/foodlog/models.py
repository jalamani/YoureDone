from django.db import models
from datetime import date
from django.utils import timezone
#from django.contrib.auth.models import User

class Food(models.Model):
    foodlist = models.ForeignKey('Foodlist', default=0, on_delete=models.CASCADE)
    food_text = models.CharField(max_length=200)
    calories = models.IntegerField(default=0)
    def __str__(self):
        return self.food_text
class Foodlist(models.Model):
    #user = models.ForeignKey('User', default=0, on_delete=models.CASCADE)
    eat_date = models.DateField('Date Eaten')
    def __str__(self):
        return str(self.eat_date)
    def was_published_recently(self):
        return self.eat_date >= timezone.now() - datetime.timedelta(days=1)
#class Users(models.User)