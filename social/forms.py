from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=30)
    password_repeat = forms.CharField(max_length=30)

    class Meta :
        model = User
        fields = ["username","phone","email"]

    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password_repeat"]:
            raise forms.ValidationError("پسورد ها با هم مطابقت ندارند")
        else:
            return cd["password_repeat"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if User.objects.filter(phone=phone).exists() :
            raise forms.ValidationError("شماره تلفن از قبل وجود دارد")
        if len(phone) != 11:
            raise forms.ValidationError("شماره تلفن صحیح نمی باشد")
        return phone

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists() :
            raise forms.ValidationError("ایمیل از قبل وجود دارد")
        return email

class TicketForm(forms.Form):

    subjects = (
        ("نظر", "نظر"),
        ("انتقاد", "انتقاد"),
        ("پیشنهاد", "پیشنهاد"),
    )

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()

    subject = forms.ChoiceField(choices=subjects)