from django import forms

class QueryForm(forms.Form):
    query_text = forms.CharField(label='Sua Query', max_length=100)
