from datetime import date
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AgregarComidaForm, NotaProgresoForm
from .models import Alimento, ItemComida, Nutricionista, Paciente, RegistroComida


# --------- helper para porcentajes de barras ---------
def _calc_percent(actual, objetivo):
    # aca calculamos el porcentaje, limitado para que la barra no se rompa
    if not objetivo or objetivo == 0:
        return 0
    pct = (actual / objetivo) * 100
    return min(int(pct), 150)


# --------- redirección segun tipo de usuario ---------
@login_required
def home_redirect(request):
    # si el usuario es nutricionista lo mandamos a su panel
    try:
        Nutricionista.objects.get(user=request.user)
        return redirect("dashboard_nutri")
    except Nutricionista.DoesNotExist:
        pass

    # si es paciente lo mandamos a su panel
    try:
        Paciente.objects.get(user=request.user)
        return redirect("dashboard_paciente")
    except Paciente.DoesNotExist:
        pass

    # si no tiene perfil, por ahora lo mandamos al admin
    return redirect("/admin/")


# --------- panel del PACIENTE ---------
@login_required
def dashboard_paciente(request):
    paciente = get_object_or_404(Paciente, user=request.user)

    hoy = date.today()
    registros_hoy = paciente.registros_comida.filter(fecha=hoy)

    calorias_hoy = sum(r.calorias_totales for r in registros_hoy)
    hierro_hoy = sum(r.hierro_total_mg for r in registros_hoy)
    b12_hoy = sum(r.b12_total_ug for r in registros_hoy)
    calorias_alcohol_hoy = sum(r.calorias_alcohol for r in registros_hoy)

    proteinas_hoy = sum(r.proteinas_totales for r in registros_hoy)
    carbohidratos_hoy = sum(r.carbohidratos_totales for r in registros_hoy)
    grasas_hoy = sum(r.grasas_totales for r in registros_hoy)

    def _calc_percent(value, target):
        if not target:
            return 0
        try:
            pct = (float(value) * 100.0) / float(target)
        except ZeroDivisionError:
            return 0
        return int(round(pct))

    calorias_pct = _calc_percent(calorias_hoy, paciente.calorias_objetivo_diarias)
    alcohol_pct = _calc_percent(calorias_alcohol_hoy, paciente.calorias_objetivo_diarias)

    # Notas visibles para el paciente
    notas_visibles = paciente.notas_progreso.filter(
        visible_para_paciente=True
    ).order_by("-fecha")[:3]

    ultima_glucemia = paciente.mediciones_glucemia.order_by("-fecha_hora").first()

    context = {
        "paciente": paciente,
        "hoy": hoy,

        "calorias_hoy": calorias_hoy,
        "hierro_hoy": hierro_hoy,
        "b12_hoy": b12_hoy,
        "calorias_alcohol_hoy": calorias_alcohol_hoy,

        "proteinas_hoy": proteinas_hoy,
        "carbohidratos_hoy": carbohidratos_hoy,
        "grasas_hoy": grasas_hoy,

        "calorias_pct": calorias_pct,
        "alcohol_pct": alcohol_pct,

        "ultima_glucemia": ultima_glucemia,

        # 👇 nuevo
        "notas_visibles": notas_visibles,
    }
    return render(request, "paciente/dashboard.html", context)



# --------- panel del NUTRICIONISTA ---------
@login_required
def dashboard_nutri(request):
    # aca buscamos el nutricionista ligado al usuario logueado
    nutri = get_object_or_404(Nutricionista, user=request.user)

    hoy = date.today()
    pacientes_data = []

    for paciente in nutri.pacientes.all():
        registros_hoy = paciente.registros_comida.filter(fecha=hoy)

        calorias_hoy = sum(r.calorias_totales for r in registros_hoy)
        hierro_hoy = sum(r.hierro_total_mg for r in registros_hoy)
        b12_hoy = sum(r.b12_total_ug for r in registros_hoy)
        calorias_alcohol_hoy = sum(r.calorias_alcohol for r in registros_hoy)

        # ultima glucemia de ese paciente
        ultima_glucemia = paciente.mediciones_glucemia.order_by(
            "-fecha_hora"
        ).first()

        pacientes_data.append(
            {
                "paciente": paciente,
                "calorias_hoy": calorias_hoy,
                "hierro_hoy": hierro_hoy,
                "b12_hoy": b12_hoy,
                "calorias_pct": _calc_percent(
                    calorias_hoy, paciente.calorias_objetivo_diarias
                ),
                "hierro_pct": _calc_percent(
                    hierro_hoy, paciente.objetivo_hierro_mg_dia
                ),
                "b12_pct": _calc_percent(
                    b12_hoy, paciente.objetivo_b12_ug_dia
                ),
                "calorias_alcohol_hoy": calorias_alcohol_hoy,
                "calorias_alcohol_pct": _calc_percent(
                    calorias_alcohol_hoy, paciente.calorias_objetivo_diarias
                ),
                "ultima_glucemia": ultima_glucemia,
            }
        )

    context = {
        "nutri": nutri,
        "hoy": hoy,
        "pacientes_data": pacientes_data,
    }
    return render(request, "nutri/dashboard.html", context)


# --------- detalle de un paciente (vista para el nutri) ---------
@login_required
def detalle_paciente(request, paciente_id):
    nutri = get_object_or_404(Nutricionista, user=request.user)
    paciente = get_object_or_404(Paciente, id=paciente_id, nutricionista=nutri)

    hoy = date.today()
    registros_hoy = paciente.registros_comida.filter(fecha=hoy)

    calorias_hoy = sum(r.calorias_totales for r in registros_hoy)
    hierro_hoy = sum(r.hierro_total_mg for r in registros_hoy)
    b12_hoy = sum(r.b12_total_ug for r in registros_hoy)
    calorias_alcohol_hoy = sum(r.calorias_alcohol for r in registros_hoy)

    def _calc_percent(value, target):
        if not target:
            return 0
        try:
            pct = (float(value) * 100.0) / float(target)
        except ZeroDivisionError:
            return 0
        return int(round(pct))

    calorias_pct = _calc_percent(calorias_hoy, paciente.calorias_objetivo_diarias)

    # --- Notas de progreso ---
    if request.method == "POST":
        form = NotaProgresoForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.paciente = paciente
            nota.nutricionista = nutri
            nota.save()
            messages.success(request, "Nota de progreso guardada correctamente.")
            return redirect("detalle_paciente", paciente_id=paciente.id)
    else:
        form = NotaProgresoForm()

    notas = paciente.notas_progreso.all()[:5]  # últimas 5
    registros_con_foto = (
        paciente.registros_comida
        .filter(
            fecha__gte=hoy - timedelta(days=7),
            foto__isnull=False,
        )
        .exclude(foto="")
        .order_by("-fecha", "-momento")[:6]
    )

    context = {
        "nutri": nutri,
        "paciente": paciente,
        "hoy": hoy,
        "calorias_hoy": calorias_hoy,
        "hierro_hoy": hierro_hoy,
        "b12_hoy": b12_hoy,
        "calorias_pct": calorias_pct,
        "calorias_alcohol_hoy": calorias_alcohol_hoy,
        "form_nota": form,
        "notas": notas,
        "registros_con_foto": registros_con_foto,
    }
    return render(request, "nutri/detalle_paciente.html", context)


# --------- formulario para que el paciente registre comida ---------
@login_required
def registrar_comida(request):
    # aca buscamos el paciente ligado al usuario logueado
    paciente = get_object_or_404(Paciente, user=request.user)

    if request.method == "POST":
        form = AgregarComidaForm(request.POST, request.FILES)
        if form.is_valid():
            fecha = form.cleaned_data["fecha"]
            momento = form.cleaned_data["momento"]
            alimento = form.cleaned_data["alimento"]
            porcion_gramos = form.cleaned_data["porcion_gramos"]
            notas = form.cleaned_data["notas"]
            foto = form.cleaned_data.get("foto")

            defaults = {"notas": notas}
            if foto:
                defaults["foto"] = foto

            # aca buscamos si ya hay un registro para esa fecha+momento
            registro, creado = RegistroComida.objects.get_or_create(
                paciente=paciente,
                fecha=fecha,
                momento=momento,
                defaults=defaults,
            )

            # si ya existia el registro y el paciente agrega notas/foto, las sumamos
            if not creado:
                changed = False
                if notas:
                    if registro.notas:
                        registro.notas += f"\n{notas}"
                    else:
                        registro.notas = notas
                    changed = True
                if foto:
                    registro.foto = foto
                    changed = True
                if changed:
                    registro.save()

            # aca creamos el item de comida con el alimento y la porcion
            ItemComida.objects.create(
                registro=registro,
                alimento=alimento,
                porcion_gramos=porcion_gramos,
            )

            messages.success(request, "La comida se registró correctamente.")
            return redirect("dashboard_paciente")
    else:
        form = AgregarComidaForm()

    return render(request, "paciente/registrar_comida.html", {"form": form})


# --------- lista de alimentos con IG y “semaforo” ---------
@login_required
def lista_alimentos(request):
    # aca mostramos todos los alimentos con su indice glucemico y semaforo
    alimentos = Alimento.objects.all().order_by("nombre")
    return render(request, "paciente/lista_alimentos.html", {"alimentos": alimentos})

