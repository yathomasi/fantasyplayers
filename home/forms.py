#importing forms
from django import forms 
 
#creating our forms
class LeagueForm(forms.Form):
 #django gives a number of predefined fields
 #CharField and EmailField are only two of them
 #go through the official docs for more field details
    league = forms.IntegerField(label='Enter your Leageu Code')
    gameweek = forms.IntegerField(label='Enter a Gameweek', max_value=38, min_value=0)
