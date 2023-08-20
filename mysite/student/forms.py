from django import forms
from student.models import Affective


class AffectiveForm(forms.ModelForm):

    class Meta:
        model = Affective
        fields = ['emoji', 'text']