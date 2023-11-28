from django import forms
from django.db.models import Model


from .models import *

class CustomCreationMixin(forms.ModelForm):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        context = kwargs.get('initial')
        for key in context.keys():
            self.fields[key].initial = context.get(key) 
        for key in self.fields.keys():
            self.fields[key].widget.attrs = {'class':"form-control"}
    
    def is_valid(self) -> bool:
        base_validation = super().is_valid()
        university = self.cleaned_data.get('university')
        name = self.cleaned_data.get('name')
        model = self.Meta.model
        if base_validation:
            try:
                model.objects.get(name=name, university=university)
            except model.DoesNotExist:
                return True
            else:
                return False
        else:
            return False    

class GroupCreationForm(CustomCreationMixin, forms.ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

class TeacherCreationForm(CustomCreationMixin, forms.ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'



class UpdateGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, model=None, fields=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = {'class':"form-control"}

class UpdateTeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = '__all__'

    def __init__(self, model=None, fields=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = {'class':"form-control"}

    