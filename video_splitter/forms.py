from django import forms

class VideoSplitForm(forms.Form):
    video = forms.FileField(label='Upload Video')
    num_parts = forms.IntegerField(label='Number of Parts')
