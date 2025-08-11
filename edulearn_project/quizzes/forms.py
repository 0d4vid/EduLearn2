from django import forms
from .models import Question, Choice

class QuestionForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        label=''
    )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = question.choices.all()
        self.fields['choice'].label = question.text
