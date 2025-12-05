from django import forms
from django.contrib import admin

from .models import (
    DietaCultural,
    Nutricionista,
    Paciente,
    Alimento,
    RegistroComida,
    ItemComida,
    MedicionGlucemia,
    EstudioLaboratorio,
    NotaProgreso,
)


# -------- PACIENTE --------

class PacienteAdminForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = "__all__"
        widgets = {
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date"}  # aca usamos el datepicker moderno
            ),
        }


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ("user", "nutricionista", "sexo", "calorias_objetivo_diarias")
    readonly_fields = ("calorias_objetivo_diarias", "imc", "edad")

    list_filter = ("sexo", "tipo_dieta", "tipo_anemia", "tipo_diabetes")
    search_fields = ("user__username", "user__first_name", "user__last_name")


# -------- NUTRICIONISTA --------

@admin.register(Nutricionista)
class NutricionistaAdmin(admin.ModelAdmin):
    list_display = ("user", "matricula", "telefono")
    search_fields = ("user__username", "user__first_name", "user__last_name", "matricula")


# -------- DIETA CULTURAL --------

@admin.register(DietaCultural)
class DietaCulturalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "region")
    search_fields = ("nombre", "region")


# -------- ALIMENTO --------

@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "calorias",
        "proteinas_g",
        "carbohidratos_g",
        "grasas_g",
        "hierro_mg",
        "b12_ug",
        "indice_glucemico",
        "categoria_ig",
    )
    search_fields = ("nombre",)
    list_filter = ("indice_glucemico",)


# -------- REGISTRO COMIDA + ITEMS --------

class ItemComidaInline(admin.TabularInline):
    model = ItemComida
    extra = 0


@admin.register(RegistroComida)
class RegistroComidaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "fecha", "momento", "calorias_totales", "hierro_total_mg", "b12_total_ug")
    list_filter = ("fecha", "momento")
    search_fields = ("paciente__user__username", "paciente__user__first_name", "paciente__user__last_name")
    inlines = [ItemComidaInline]

@admin.register(ItemComida)
class ItemComidaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "registro",
        "alimento",
        "porcion_gramos",
        "calorias_porcion",
        "hierro_porcion_mg",
        "b12_porcion_ug",
        "calorias_alcohol_porcion",
    )

    def calorias_porcion(self, obj):
        return round(obj.calorias_para_esta_porcion, 1)
    calorias_porcion.short_description = "kcal porción"

    def hierro_porcion_mg(self, obj):
        return round(obj.hierro_para_esta_porcion_mg, 2)
    hierro_porcion_mg.short_description = "Fe (mg) porción"

    def b12_porcion_ug(self, obj):
        return round(obj.b12_para_esta_porcion_ug, 2)
    b12_porcion_ug.short_description = "B12 (µg) porción"

    def calorias_alcohol_porcion(self, obj):
        return round(obj.calorias_alcohol_para_esta_porcion, 1)
    calorias_alcohol_porcion.short_description = "kcal alcohol"



# -------- GLUCEMIA --------

@admin.register(MedicionGlucemia)
class MedicionGlucemiaAdmin(admin.ModelAdmin):
    list_display = ("paciente", "fecha_hora", "valor_mg_dl", "contexto")
    list_filter = ("fecha_hora",)
    search_fields = ("paciente__user__username", "paciente__user__first_name", "paciente__user__last_name")


# -------- ESTUDIOS DE LABORATORIO --------

@admin.register(EstudioLaboratorio)
class EstudioLaboratorioAdmin(admin.ModelAdmin):
    list_display = ("paciente", "tipo", "valor", "unidad", "fecha")
    list_filter = ("tipo", "fecha")
    search_fields = ("paciente__user__username", "paciente__user__first_name", "paciente__user__last_name")

@admin.register(NotaProgreso)
class NotaProgresoAdmin(admin.ModelAdmin):
    list_display = ("fecha", "paciente", "nutricionista", "titulo", "visible_para_paciente")
    list_filter = ("fecha", "nutricionista", "visible_para_paciente")
    search_fields = ("texto", "titulo", "paciente__user__username", "paciente__user__first_name")
