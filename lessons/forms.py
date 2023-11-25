from typing import Any
from django import forms


from .models import Lesson

class LessonCretionForm(forms.ModelForm):

    class Meta:
        model = Lesson
        fields = '__all__'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        context = kwargs.get('initial')
        for key in context.keys():
            self.fields[key].initial = context.get(key) 

    def is_valid(self) -> bool:
        base_validation = super().is_valid() 

        groups = self.cleaned_data['group']
        day = self.cleaned_data['day']
        num_lesson = self.cleaned_data['num_lesson']
        num_week = self.cleaned_data['num_week']
        is_session = self.cleaned_data['is_session'] 

        for group in groups:
            try:
                lesson = Lesson.objects.get(group=group, num_lesson=num_lesson, num_week=num_week, is_session=is_session, day_id=day.pk)
                if lesson:
                    return False
            except Lesson.DoesNotExist:
                if not base_validation:
                    return False
                else:
                    continue
        else:
            return True