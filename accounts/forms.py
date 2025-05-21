from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, UserPreference

class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField(required=True)
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 4}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'birth_date', 'bio', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating user profile.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'birth_date', 'bio', 'profile_picture')

class UserPreferenceForm(forms.ModelForm):
    """
    Form for managing user's news preferences
    """
    categories = forms.MultipleChoiceField(
        choices=UserPreference.CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select your preferred news categories"
    )
    
    keywords = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., AI, Climate Change, Space Exploration',
            'class': 'form-control'
        }),
        help_text="Enter keywords separated by commas"
    )
    
    excluded_sources = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., source1.com, source2.com',
            'class': 'form-control'
        }),
        help_text="Enter news sources to exclude, separated by commas"
    )

    class Meta:
        model = UserPreference
        fields = ['categories', 'keywords', 'excluded_sources']

    def clean_categories(self):
        categories = self.cleaned_data.get('categories', [])
        return list(categories)  # Convert to list for JSON storage 