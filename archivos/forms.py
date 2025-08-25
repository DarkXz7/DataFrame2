from django import forms

class SubidaArchivoForm(forms.Form):
    archivo = forms.FileField()