from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Reset, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from .models import Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'author']

    def __init__(self, *args, **kwargs):
        # print('CreatePostForm:', args, kwargs)
        super(CreatePostForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout = Layout(
            Field('title', css_class='input-xlarge'),
            Field('content', rows="3", css_class='input-xlarge'),
            Field('author', type='hidden'),
            FormActions(
                Submit('create', 'Создать', css_class='btn-primary'),
                Button('cancel', 'Не, не надо', onclick='history.go(-1);'),
            )
        )


class PublicateConfirm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PublicateConfirm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            FormActions(
                Submit('publish', 'Опубликовать', css_class='btn-primary'),
                Button('cancel', 'Передумал', onclick='history.go(-1);'),
            )
        )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-6'
        self.helper.layout = Layout(
            # 'username',
            # 'password',
            Field('username', css_class='input-xlarge'),
            Field('password', css_class='input-xlarge'),
            ButtonHolder(
                Submit('login', 'Войти', css_class='btn-primary')
            )
        )


