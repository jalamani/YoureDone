from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User

class Food(models.Model):
    foodlist = models.ForeignKey('Foodlist', default=0, on_delete=models.CASCADE)
    food_text = models.CharField(max_length=20,default='NA')
    calories = models.IntegerField(default=0)
    def __str__(self):
        return self.food_text
class Foodlist(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE) # id 2 is admin
    eat_date = models.DateField('Date Eaten',default=date.today)
    def __str__(self):
        return str(self.eat_date)
    def was_published_recently(self):
        return self.eat_date >= timezone.now() - datetime.timedelta(days=1)
#class Users(models.User)