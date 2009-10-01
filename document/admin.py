from django.contrib import admin
from models import Document
from django import forms

class DocumentAdmin(admin.ModelAdmin):
    model = Document

admin.site.register(Document, DocumentAdmin)
