from django import forms
from .models import Post
from editormd.widget import EditorMdWidget


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'desc': forms.Textarea(),
            'content': EditorMdWidget(),
        }
        # fields = '__all__'
        exclude = ['author']
