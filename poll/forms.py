from django import forms

from poll.models import Poll, PollOption


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ['option']
        widgets = {
            'option': forms.TextInput(attrs={'class': 'form-control'})
        }
