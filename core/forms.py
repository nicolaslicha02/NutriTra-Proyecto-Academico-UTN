from django import forms
from .models import Alimento, RegistroComida, NotaProgreso


class AgregarComidaForm(forms.Form):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )

    momento = forms.ChoiceField(
        choices=RegistroComida.Momento.choices
    )

    alimento = forms.ModelChoiceField(
        queryset=Alimento.objects.all()
    )

    porcion_gramos = forms.DecimalField(
        max_digits=6,
        decimal_places=1,
        min_value=1,
        label="Porción (en gramos)",
    )

    notas = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Notas (opcional)",
    )

    foto = forms.ImageField(
        required=False,
        label="Foto de la comida (opcional)",
    )


class NotaProgresoForm(forms.ModelForm):
    class Meta:
        model = NotaProgreso
        fields = ["titulo", "texto", "visible_para_paciente"]
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Ej: Semana 1 – Ajuste de calorías",
            }),
            "texto": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Comentario sobre el progreso, adherencia al plan, sugerencias, etc.",
            }),
            "visible_para_paciente": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }
