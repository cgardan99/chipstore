from allauth.account.forms import SignupForm
from django import forms
from chipstore.utils.common import get_image_directory_path

class _SignupForm(SignupForm):
    name = forms.CharField(
        label="Nombre",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Introduce tu nombre completo"}),
    )
    foto = forms.FileField(
        label="Foto de Perfil",
        required=True,
        widget=forms.FileInput(
            attrs={
                "placeholder": "Introduce una fotografía",
                "accept": "image/x-png,image/gif,image/jpeg",
            }
        ),
    )

    def save(self, request):
        user = super(_SignupForm, self).save(request)
        user.name = self.cleaned_data["name"]
        user.foto = self.cleaned_data["foto"]
        user.save()
        return user