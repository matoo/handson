from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, ValidationError
from django.utils.translation import ugettext as _
from .models import Questionnaire, DIFFICULT_POINTS_CHOICES


# Refered from: https://gist.github.com/romulocollopy/bffe38fa72af5bc427e1
class CommaSeparatedSelectInteger(forms.MultipleChoiceField):
    def to_python(self, value):
        if not value:
            return ''
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(
                self.error_messages['invalid_list'], code='invalid_list'
            )
        l = []
        for val in value:
          try:
            n = int(val)
          except ValueError:
            continue
          l.append(val)
        return ','.join([str(val) for val in l])

    def validate(self, value):
        """
        Validates that the input is a string of integers separeted by comma.
        """
        if self.required and not value:
            raise ValidationError(
                self.error_messages['required'], code='required'
            )

        # Validate that each value in the value list is in self.choices.
        for val in value.split(','):
            if not self.valid_value(val):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )

    def prepare_value(self, value):
        """ Convert the string of comma separated integers in list"""
        if not value:
          return ''
        #return value.split(',')
        return ','.join([str(val) for val in value])

      
class QuestionnaireForm(forms.ModelForm):

  difficult_points = CommaSeparatedSelectInteger(
    choices=[('', '無回答')] + [(i[0], i[1]) for i in DIFFICULT_POINTS_CHOICES],
    widget=forms.CheckboxSelectMultiple(),
    required=False,
  )

  class Meta:
    model = Questionnaire
    exclude = ['user']
    widgets = {
      'how_about_handson':  forms.Textarea(attrs={'class': 'form-control'}),
      'difficult_other':    forms.Textarea(attrs={'class': 'form-control'}),
      'time_settings':      forms.Select(attrs={'class': 'form-control'}),
      'handson_level':      forms.Select(attrs={'class': 'form-control'}),
      'handson_interest':   forms.Select(attrs={'class': 'form-control'}),
      'handson_quantity':   forms.Select(attrs={'class': 'form-control'}),
      'free_opinions':      forms.Textarea(attrs={'class': 'form-control'}),
      'interest_trainings': forms.Textarea(attrs={'class': 'form-control'}),
    }

    
class LoginForm(forms.Form):
  username = forms.CharField(label='Username', required=True, widget=forms.TextInput)
  password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

  def clean_username(self):
    username = self.cleaned_data['username']
    if username and not User.objects.filter(username=username).exists():
      raise forms.ValidationError('Username is wrong')
    return username

  def clean_password(self):
    password = self.cleaned_data['password']
    if not password:
      raise forms.ValidatonError('Password is wrong')
    if 'username' not in self.cleaned_data:
      return password
    username = self.cleaned_data['username']
    user = User.objects.filter(username=username).first()
    if not user.check_password(password):
      raise forms.ValidationError('Password is wrong')
    return password
