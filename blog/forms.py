from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Войти', css_class='btn-primary')
            )
        )


class PublicateConfirm():
    def __init__(self, *args, **kwargs):
        super(PublicateConfirm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout(
            ButtonHolder(
                Submit('publish', 'Опубликовать', css_class='btn-primary'),
                Button('cancel', 'Передумал'),
            )
        )
