from django import forms
from datetime import date, datetime
from task_app.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'},format='%Y-%m-%dT%H:%M'),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['due_date'].input_formats = ['%Y-%m-%dT%H:%M']


class TaskTodayForm(forms.ModelForm):
    time = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'time']

    def save(self, commit=True):
        instance = super().save(commit=False)
        selected_time = self.cleaned_data['time']
        instance.due_date = datetime.combine(date.today(), selected_time)
        print("Saving due_date:", instance.due_date)
        if commit:
            instance.save()
        return instance
