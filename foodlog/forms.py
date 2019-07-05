from django import forms

class newfoodForm(forms.Form):
    newFood = forms.CharField(label='New food', max_length=100)
    newCalories = forms.IntegerField(label="New food's calories", min_value=0, max_value=99999)
class newlogForm(forms.Form):
	newLog = forms.DateField(label='New date')#, max_length=100)
class searchdatabaseForm(forms.Form):
	databaseSearch = forms.CharField(label='Search field', max_length=100)