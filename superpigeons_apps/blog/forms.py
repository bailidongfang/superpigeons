from django import forms

from other_apps.ckeditor_uploader.fields import RichTextUploadingFormField


# from superpigeons_apps.user.models import UserInfo


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

