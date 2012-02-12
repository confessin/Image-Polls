from django import forms

from main import models

class UploadForm(forms.ModelForm):
    class Meta:
        model = models.UserImage
        fields = (
                'image',
                )
