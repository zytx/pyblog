from django import forms
from .models import Article


class ArticleAdminForm(forms.ModelForm):

    class Meta:
        model = Article
        widgets = {
            'desc': forms.Textarea(),
        }
        fields = '__all__'