from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'email', 'dob', 'age', 'gender', 'course',
            'address', 'phone', 'previous_marks'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[
                ('Male', 'Male'),
                ('Female', 'Female'),
                ('Other', 'Other')
            ]),
            'previous_marks': forms.NumberInput(attrs={'step': 0.01, 'min': 0}),
            'age': forms.NumberInput(attrs={'min': 0}),
        }

    # ✅ Validation to ensure previous_marks is entered
    def clean_previous_marks(self):
        marks = self.cleaned_data.get('previous_marks')
        if marks is None:
            raise forms.ValidationError("Please enter previous marks")
        if marks < 0:
            raise forms.ValidationError("Marks cannot be negative")
        return marks

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is None or age <= 0:
            raise forms.ValidationError("Please enter a valid age")
        return age
