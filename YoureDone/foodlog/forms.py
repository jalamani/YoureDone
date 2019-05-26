from django import forms

class newfoodForm(forms.Form):
    newFood = forms.CharField(label='New food', max_length=100, required=False)
    newCalories = forms.IntegerField(label="New food's calories", min_value=0, max_value=99999, required=False )
class newlogForm(forms.Form):
	newLog = forms.DateField(label='New date',required=False)#, max_length=100)