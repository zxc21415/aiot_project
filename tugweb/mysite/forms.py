from django import forms
from mysite.models import ImageModel


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image']
        # widgets = {
        #     'image': forms.FileInput(attrs={'class': 'form-control-file'})
        # }