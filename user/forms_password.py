from django import forms

class FindPasswordForm(forms.Form):
    phone_number = forms.CharField(label='전화번호', max_length=15)

class VerifyCodeForm(forms.Form):
    code = forms.CharField(label='인증번호', max_length=6)

class ResetPasswordForm(forms.Form):
    new_password1 = forms.CharField(label='새 비밀번호', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='새 비밀번호 확인', widget=forms.PasswordInput)
