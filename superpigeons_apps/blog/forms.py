from django import forms
from django.core.exceptions import ValidationError
from ckeditor_uploader.fields import RichTextUploadingFormField
from ckeditor.widgets import CKEditorWidget
# from superpigeons_apps.user.models import UserInfo
import re


class WriteArticle(forms.Form):
    # 写博客表单
    title = forms.CharField(
        required=True,
        max_length=50,
        min_length=6,
        error_messages={'required': u'请输入标题'},
        widget=forms.TextInput(attrs={'placeholder': u'标题', 'id': u'title'}),
    )
    text = RichTextUploadingFormField()

