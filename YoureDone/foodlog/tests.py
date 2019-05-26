from django.test import TestCase
from .models import Foodlist, Food
# Create your tests here.
class FoodModelTests(TestCase):

    def test_positive_calories(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """        
        testFood = Food(food_text = test, calories = 0)
        testFood.calories -= 30
        self.assertIs(testFood.calories>=0, False)