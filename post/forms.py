from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tech_stack', 'github_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'post-input', 'placeholder': '제목'}),
            'content': forms.Textarea(attrs={'class': 'post-textarea', 'placeholder': '내용'}),
            'tech_stack': forms.TextInput(attrs={'class': 'post-input', 'placeholder': '기술 스택 선택'}),
            'github_link': forms.TextInput(attrs={'class': 'post-input', 'placeholder': '깃허브 링크'}),
        }
