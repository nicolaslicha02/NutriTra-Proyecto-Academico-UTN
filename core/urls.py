from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_redirect, name="home"),

    # panel paciente
    path("paciente/dashboard/", views.dashboard_paciente, name="dashboard_paciente"),
    path(
        "paciente/registrar-comida/",
        views.registrar_comida,
        name="registrar_comida",
    ),
    path(
        "paciente/alimentos/",
        views.lista_alimentos,
        name="lista_alimentos",
    ),

    # panel nutricionista
    path("nutri/dashboard/", views.dashboard_nutri, name="dashboard_nutri"),
    path(
        "nutri/paciente/<int:paciente_id>/",
        views.detalle_paciente,
        name="detalle_paciente",
    ),
]

