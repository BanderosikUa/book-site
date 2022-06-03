from urllib import request
from attr import attr
from django import forms

class CommentCreateForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
                                    attrs={
                                        'rows': 4,
                                        'placeholder': 'Comment',
                                        'id': 'body-comment',
                                        'class': "form-control form-control-lg"
                                    }), required=True, label=False)
