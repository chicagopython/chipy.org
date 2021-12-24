from captcha.fields import CaptchaTextInput


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = "custom_captcha/widget.html"
