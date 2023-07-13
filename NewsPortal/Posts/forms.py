from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Author


class NWForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['many_author', 'header', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        header = cleaned_data.get("header")

        if header == text:
            raise ValidationError(
                "Содержание не должно быть идентично заголовку !"
            )

        return cleaned_data


class ATForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['many_author', 'header', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        header = cleaned_data.get("header")

        if header == text:
            raise ValidationError(
                "Содержание не должно быть идентично заголовку !"
            )

        return cleaned_data
