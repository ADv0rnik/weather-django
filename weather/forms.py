from django import forms


class InputForm(forms.Form):
    region_name = forms.CharField(label='Region',
                                  max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-input'}))
