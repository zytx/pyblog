from django import forms
from .models import Article
from editormd.widget import EditormdWidget


class ArticleAdminForm(forms.ModelForm):

    class Meta:
        model = Article
        widgets = {
            'desc': forms.Textarea(),
            'content': EditormdWidget(),
        }
        fields = '__all__'
        #exclude = ['author']