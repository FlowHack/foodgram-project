from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def clean_password(self):
        form_data = self.cleaned_data
        password = form_data['password']
        if len(password) < 8:
            self._errors['password'] = [
                'Пароль должен быть длиннее 8 символов'
            ]
            del form_data['password']

        return form_data
