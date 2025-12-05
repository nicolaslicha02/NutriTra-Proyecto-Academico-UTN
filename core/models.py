from decimal import Decimal
from datetime import date

from django.contrib.auth.models import User
from django.db import models



class DietaCultural(models.Model):
    # aca guardamos un tipo de dieta segun una cultura o region
    nombre = models.CharField(max_length=100)   # ej: Mediterránea, Andina
    region = models.CharField(
        max_length=100,
        null=True,
        blank=True,                             # ej: Europa, Latinoamérica
    )
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Nutricionista(models.Model):
    # este modelo extiende al usuario cuando es nutricionista
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        nombre = self.user.get_full_name() or self.user.username
        return f"Nutricionista: {nombre}"


class DietaCultural(models.Model):
    # aca guardamos un tipo de dieta segun una cultura o region
    nombre = models.CharField(max_length=100)   # ej: Mediterránea, Andina
    region = models.CharField(
        max_length=100,
        null=True,
        blank=True,                             # ej: Europa, Latinoamérica
    )
    descripcion = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nombre


class Nutricionista(models.Model):
    # este modelo extiende al usuario cuando es nutricionista
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=50, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        nombre = self.user.get_full_name() or self.user.username
        return f"Nutricionista: {nombre}"


class Paciente(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMENINO = "F", "Femenino"
        OTRO = "O", "Otro"

    class ObjetivoPeso(models.TextChoices):
        BAJAR = "BAJAR", "Bajar de peso"
        MANTENER = "MANTENER", "Mantener peso"
        SUBIR = "SUBIR", "Subir de peso"

    class TipoDieta(models.TextChoices):
        OMNIVORO = "OMNIVORO", "Omnívoro"
        VEGETARIANO = "VEGETARIANO", "Vegetariano"
        VEGANO = "VEGANO", "Vegano"
        CARNIVORO = "CARNIVORO", "Carnívoro"

    class TipoAnemia(models.TextChoices):
        NINGUNA = "NINGUNA", "Sin anemia"
        FERROPENICA = "FERROPENICA", "Anemia ferropénica"
        MEGALOBLASTICA = "MEGALOBLASTICA", "Anemia megaloblástica"
        HEMOLITICA = "HEMOLITICA", "Anemia hemolítica"

    class TipoDiabetes(models.TextChoices):
        NINGUNA = "NINGUNA", "Sin diabetes"
        TIPO1 = "TIPO1", "Diabetes tipo 1"
        TIPO2 = "TIPO2", "Diabetes tipo 2"
        OTRO = "OTRO", "Otra"

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nutricionista = models.ForeignKey(
        "Nutricionista",
        on_delete=models.CASCADE,
        related_name="pacientes",
    )

    sexo = models.CharField(max_length=1, choices=Sexo.choices)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    # antropometría
    peso_actual = models.DecimalField(
        max_digits=5, decimal_places=1, null=True, blank=True, help_text="kg"
    )
    talla_m = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True, help_text="m"
    )

    # estilo alimentario y patología
    tipo_dieta = models.CharField(
        max_length=20,
        choices=TipoDieta.choices,
        default=TipoDieta.OMNIVORO,
    )
    tipo_anemia = models.CharField(
        max_length=20,
        choices=TipoAnemia.choices,
        default=TipoAnemia.NINGUNA,
    )
    tipo_diabetes = models.CharField(
        max_length=20,
        choices=TipoDiabetes.choices,
        default=TipoDiabetes.NINGUNA,
    )

    # objetivo de peso
    objetivo_peso_tipo = models.CharField(
        max_length=10,
        choices=ObjetivoPeso.choices,
        default=ObjetivoPeso.MANTENER,
    )

    # 🔹 factor de actividad (afecta a Mifflin)
    factor_actividad = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("1.40"),
        help_text="Ej: 1.2 sedentario, 1.4 ligero, 1.6 moderado, 1.8 muy activo",
    )

    # objetivos diarios (se calculan en gran parte en base a Mifflin)
    calorias_objetivo_diarias = models.IntegerField(
        null=True, blank=True, help_text="kcal/día (se calcula automático)"
    )
    objetivo_hierro_mg_dia = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    objetivo_b12_ug_dia = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )

    def __str__(self):
        nombre = self.user.get_full_name() or self.user.username
        return f"Paciente: {nombre}"

    # ---- propiedades calculadas ----

    @property
    def edad(self):
        if not self.fecha_nacimiento:
            return None
        hoy = date.today()
        return hoy.year - self.fecha_nacimiento.year - (
            (hoy.month, hoy.day)
            < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    @property
    def imc(self):
        # aca calculamos el IMC si tenemos peso y altura
        if self.peso_actual and self.talla_m:
            try:
                return round(
                    float(self.peso_actual) / (float(self.talla_m) ** 2), 1
                )
            except ZeroDivisionError:
                return None
        return None
    @property
    def clasificacion_imc(self):
        """
        Clasificación simple según IMC (OMS):
        Bajo peso, Normopeso, Sobrepeso, Obesidad I/II/III
        """
        bmi = self.imc
        if bmi is None:
            return None

        try:
            bmi = float(bmi)
        except (TypeError, ValueError):
            return None

        if bmi < 18.5:
            return "Bajo peso"
        elif bmi < 25:
            return "Normopeso"
        elif bmi < 30:
            return "Sobrepeso"
        elif bmi < 35:
            return "Obesidad grado I"
        elif bmi < 40:
            return "Obesidad grado II"
        else:
            return "Obesidad grado III"


    @property
    def estado_nutricional(self):
        # texto muy general por ahora
        if self.tipo_anemia != self.TipoAnemia.NINGUNA:
            return f"Anemia {self.get_tipo_anemia_display()}"
        return "Nutrición normal en el adulto"

    # ---- formulas de calorías (Mifflin) ----

    def calorias_mantenimiento_mifflin(self):
        # aca calculamos el gasto de mantenimiento con Mifflin-St Jeor
        if not (self.peso_actual and self.talla_m and self.edad is not None):
            return None

        peso = float(self.peso_actual)
        altura_cm = float(self.talla_m) * 100
        edad = self.edad

        if self.sexo == self.Sexo.MASCULINO:
            bmr = 10 * peso + 6.25 * altura_cm - 5 * edad + 5
        else:
            # mujeres y otros caen en esta rama para simplificar
            bmr = 10 * peso + 6.25 * altura_cm - 5 * edad - 161

        factor = float(self.factor_actividad or 1.4)
        return int(round(bmr * factor))

    def calcular_calorias_objetivo(self):
        # aca ajustamos segun si quiere bajar, subir o mantener
        mantenimiento = self.calorias_mantenimiento_mifflin()
        if mantenimiento is None:
            return None

        if self.objetivo_peso_tipo == self.ObjetivoPeso.SUBIR:
            return int(round(mantenimiento * 1.2))
        elif self.objetivo_peso_tipo == self.ObjetivoPeso.BAJAR:
            return int(round(mantenimiento * 0.8))
        else:
            return mantenimiento

    def save(self, *args, **kwargs):
        # antes de guardar calculamos las calorias objetivo
        objetivo = self.calcular_calorias_objetivo()
        if objetivo is not None:
            self.calorias_objetivo_diarias = objetivo
        super().save(*args, **kwargs)




class Alimento(models.Model):
    nombre = models.CharField(max_length=100)

    calorias = models.DecimalField(max_digits=6, decimal_places=1, help_text="kcal / 100 g")
    proteinas_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    carbohidratos_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    grasas_g = models.DecimalField(max_digits=6, decimal_places=1, default=0)

    hierro_mg = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, help_text="mg / 100 g"
    )
    b12_ug = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, help_text="µg / 100 g"
    )

    indice_glucemico = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="0–100 aprox. Bajo <55, medio 55–69, alto ≥70",
    )

    es_bebida_alcoholica = models.BooleanField(
        default=False,
        help_text="Marcar si la mayor parte de las calorias vienen del alcohol (vino, cerveza, etc.)",
    )
    gramos_alcohol_100g = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        default=0,
        help_text="g de alcohol puro aprox. por 100 ml (ABV × 0,8)",
    )

    # ---- helpers para ItemComida (en DECIMAL, no float) ----
    @property
    def calorias_kcal_100g(self):
        base = getattr(self, "calorias", None)
        return base if base is not None else Decimal("0")

    @property
    def hierro_mg_100g(self):
        base = getattr(self, "hierro_mg", None)
        return base if base is not None else Decimal("0")

    @property
    def b12_ug_100g(self):
        base = getattr(self, "b12_ug", None)
        return base if base is not None else Decimal("0")

    def __str__(self):
        return self.nombre

    def categoria_ig(self):
        if self.indice_glucemico is None:
            return "Sin dato"
        ig = self.indice_glucemico
        if ig < 55:
            return "Bajo"
        elif ig < 70:
            return "Medio"
        return "Alto"



# ----------------- REGISTRO DE COMIDA -----------------

class RegistroComida(models.Model):
    class Momento(models.TextChoices):
        DESAYUNO = "DES", "Desayuno"
        ALMUERZO = "ALM", "Almuerzo"
        MERIENDA = "MER", "Merienda"
        CENA = "CEN", "Cena"
        SNACK = "SNA", "Snack"

    paciente = models.ForeignKey(
        "Paciente",
        on_delete=models.CASCADE,
        related_name="registros_comida",
    )
    fecha = models.DateField()
    momento = models.CharField(max_length=3, choices=Momento.choices)

    notas = models.TextField(blank=True, default="")

    # foto opcional del plato
    foto = models.ImageField(
        upload_to="comidas/",
        null=True,
        blank=True,
        help_text="Foto opcional del plato o comida.",
    )

    def __str__(self):
        return f"{self.paciente} - {self.fecha} ({self.get_momento_display()})"

    # --- PROPIEDADES CALCULADAS ---

    @property
    def calorias_totales(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.calorias_para_esta_porcion
        return total

    @property
    def hierro_total_mg(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.hierro_para_esta_porcion_mg
        return total

    @property
    def b12_total_ug(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.b12_para_esta_porcion_ug
        return total

    @property
    def calorias_alcohol(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.calorias_alcohol_para_esta_porcion
        return total

    # 🔹 NUEVO: totales de macros del registro
    @property
    def proteinas_totales(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.proteinas_para_esta_porcion_g
        return total

    @property
    def carbohidratos_totales(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.carbohidratos_para_esta_porcion_g
        return total

    @property
    def grasas_totales(self):
        total = Decimal("0")
        for item in self.items.all():
            total += item.grasas_para_esta_porcion_g
        return total

    class Meta:
        ordering = ["-fecha", "-momento", "id"]
        unique_together = ("paciente", "fecha", "momento")



class ItemComida(models.Model):
    registro = models.ForeignKey(
        RegistroComida,
        on_delete=models.CASCADE,
        related_name="items",
    )
    alimento = models.ForeignKey("Alimento", on_delete=models.CASCADE)
    porcion_gramos = models.DecimalField(max_digits=6, decimal_places=1)

    def __str__(self):
        return f"{self.alimento} ({self.porcion_gramos} g)"

    # --------- helpers por porción ---------
    @property
    def calorias_para_esta_porcion(self):
        if not self.alimento.calorias_kcal_100g:
            return Decimal("0")
        return (Decimal(str(self.alimento.calorias_kcal_100g)) * self.porcion_gramos) / Decimal("100")

    @property
    def hierro_para_esta_porcion_mg(self):
        if not self.alimento.hierro_mg_100g:
            return Decimal("0")
        return (Decimal(str(self.alimento.hierro_mg_100g)) * self.porcion_gramos) / Decimal("100")

    @property
    def b12_para_esta_porcion_ug(self):
        if not self.alimento.b12_ug_100g:
            return Decimal("0")
        return (Decimal(str(self.alimento.b12_ug_100g)) * self.porcion_gramos) / Decimal("100")

    @property
    def calorias_alcohol_para_esta_porcion(self):
        if (
            not self.alimento.es_bebida_alcoholica
            or not self.alimento.gramos_alcohol_100g
        ):
            return Decimal("0")

        gramos = (self.alimento.gramos_alcohol_100g * self.porcion_gramos) / Decimal("100")
        return gramos * Decimal("7") 

    # 🔹 NUEVO: macros por porción (en gramos)
    @property
    def proteinas_para_esta_porcion_g(self):
        if not self.alimento.proteinas_g:
            return Decimal("0")
        return (self.alimento.proteinas_g * self.porcion_gramos) / Decimal("100")

    @property
    def carbohidratos_para_esta_porcion_g(self):
        if not self.alimento.carbohidratos_g:
            return Decimal("0")
        return (self.alimento.carbohidratos_g * self.porcion_gramos) / Decimal("100")

    @property
    def grasas_para_esta_porcion_g(self):
        if not self.alimento.grasas_g:
            return Decimal("0")
        return (self.alimento.grasas_g * self.porcion_gramos) / Decimal("100")






class MedicionGlucemia(models.Model):
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="mediciones_glucemia"
    )
    fecha_hora = models.DateTimeField()
    valor_mg_dl = models.DecimalField(max_digits=5, decimal_places=1)
    contexto = models.CharField(
        max_length=50, blank=True, help_text="ej: ayunas, posprandial..."
    )

    def __str__(self):
        return f"{self.paciente} - {self.valor_mg_dl} mg/dL ({self.fecha_hora})"

    # ---- semáforo ----
    def estado_semaforo(self):
        v = float(self.valor_mg_dl)
        if v < 70:
            return "bajo"
        elif 70 <= v <= 99:
            return "normal"
        elif 100 <= v <= 125:
            return "pre"
        else:
            return "alto"

    def color_bootstrap(self):
        estado = self.estado_semaforo()
        if estado == "normal":
            return "success"   # verde
        elif estado == "pre":
            return "warning"   # amarillo
        else:
            return "danger"    # rojo

class EstudioLaboratorio(models.Model):
    # aca guardamos estudios de laboratorio simples relacionados a anemia u otros controles

    TIPO_ESTUDIO_CHOICES = [
        ("HB", "Hemoglobina"),
        ("FERRITINA", "Ferritina"),
        ("HEMATOCRITO", "Hematocrito"),
        ("OTRO", "Otro"),
    ]

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name="estudios",
    )
    tipo = models.CharField(max_length=20, choices=TIPO_ESTUDIO_CHOICES)
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    unidad = models.CharField(
        max_length=20,
        default="g/dL",   # la unidad real depende del tipo de estudio
    )
    fecha = models.DateField()
    notas = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.paciente} - {self.get_tipo_display()} ({self.fecha})"
    
class NotaProgreso(models.Model):
    """
    Nota corta del nutricionista para un paciente.
    Sirve para ir registrando el seguimiento semanal/mensual.
    """
    paciente = models.ForeignKey(
        "Paciente",
        on_delete=models.CASCADE,
        related_name="notas_progreso",
    )
    nutricionista = models.ForeignKey(
        "Nutricionista",
        on_delete=models.CASCADE,
        related_name="notas_escritas",
    )

    fecha = models.DateField(auto_now_add=True)
    titulo = models.CharField(max_length=100, blank=True)
    texto = models.TextField()

    visible_para_paciente = models.BooleanField(
        default=True,
        help_text="Si está tildado, en el futuro se podría mostrar en el panel del paciente.",
    )

    class Meta:
        ordering = ["-fecha", "-id"]

    def __str__(self):
        base = self.titulo or (self.texto[:30] + "...")
        return f"Nota {self.fecha} - {self.paciente}: {base}"

