from django.contrib import admin
from models import Picture 
from django import forms
from tools.AdminImageWidget import AdminImageWidget

class ImageUploadForm(forms.ModelForm):
    file = forms.FileField(widget=AdminImageWidget)
    class Meta:
        model = Picture

class PictureInline(admin.TabularInline):
    model = Picture
    form = ImageUploadForm
    extra = 1

class PictureAdmin(admin.ModelAdmin):
    form = ImageUploadForm
    model = Picture


admin.site.register(Picture, PictureAdmin)
