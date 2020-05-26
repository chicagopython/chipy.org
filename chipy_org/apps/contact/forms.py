from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField

class ContactForm(forms.Form):
    sender = forms.CharField(label="From")
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = NoReCaptchaField()

    def send_email(self):
        pass
