from django import forms
from .models import Task, CustomUser, AssignmentGroup
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',) 


class AssignmentGroupForm(forms.ModelForm):
    class Meta:
        model = AssignmentGroup
        fields = ['name', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['task_token', 'title', 'description', 'due_date', 'priority', 'status', 'creator', 'assignment_group', 'assigned_to']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.Select(choices=self.fields['status'].choices)
        self.fields['priority'].widget = forms.Select(choices=self.fields['priority'].choices)
        self.fields['assignment_group'].queryset = AssignmentGroup.objects.all()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_token', 'title', 'description', 'due_date', 'priority', 'status', 'creator', 'assignment_group', 'assigned_to']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget = forms.Select(choices=self.fields['status'].choices)
        self.fields['priority'].widget = forms.Select(choices=self.fields['priority'].choices)
        self.fields['assigned_to'].required = False
        self.fields['assignment_group'].queryset = AssignmentGroup.objects.all()

