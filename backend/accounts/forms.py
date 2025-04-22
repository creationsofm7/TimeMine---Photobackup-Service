from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    
        class Meta(UserCreationForm):
            model = CustomUser
            fields = UserCreationForm.Meta.fields + ('email', 'username', 'name')

class CustomUserChangeForm(UserChangeForm):
        
        class Meta(UserChangeForm):
            model = CustomUser
            fields = {
                'email',
                'username',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
                'storage',
                'is_premium'
            }





