from django.test import TestCase
from foodlog.models import Foodlist, Food
# Create your tests here.
class FoodModelTests(TestCase):

    def test_positive_calories(self):    
        testFood = Food(food_text = "test", calories = -30)
        self.assertIs(testFood.calories>=0, False)
    def emptyfoodFields(self):    
        testFood = Food()
        self.assertIs(testFood.id>=0, False)
        