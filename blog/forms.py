from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Button, Reset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Войти', css_class='btn-primary')
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
