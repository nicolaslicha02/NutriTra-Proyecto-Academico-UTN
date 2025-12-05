# NutriTra – Plataforma de seguimiento nutricional

NutriTra es una aplicación web hecha con **Django** que usamos como nexo entre **nutricionistas** y **pacientes**.  
La idea es simple: dejar de depender de “me parece que comí bien” y empezar a trabajar con datos concretos sobre lo que el paciente consume cada día.

Proyecto académico desarrollado como trabajo práctico en la **UTN – Facultad Regional La Plata**.

---

## ¿Qué problema apunta a resolver?

En una consulta típica el nutricionista pregunta cómo viene comiendo el paciente y la respuesta suele ser a memoria.  
Con NutriTra buscamos organizar esa información:

- El profesional puede:
  - Registrar pacientes.
  - Cargar sus ingestas diarias.
  - Ver un resumen del día con calorías y porcentajes.
- El paciente termina teniendo un registro más ordenado de lo que consume, que se usa como apoyo en la consulta.

---

## Funcionalidades principales (versión actual)

### Gestión de pacientes

- Alta, baja y modificación de pacientes.
- Datos básicos de identificación.
- Pensado para que cada nutricionista tenga su cartera de pacientes en un solo lugar.

### Registro de ingestas

Para cada paciente y cada día se registran las comidas:

- Descripción del alimento o bebida.
- Cantidad / porción.
- Calorías estimadas.
- Posibilidad de marcar si aporta **calorías desde alcohol**.

Con esa información el sistema calcula:

- Calorías totales del día.
- Porcentaje respecto al objetivo diario estimado.
- Porcentaje de calorías que vienen del alcohol.

### Dashboard diario

Pantalla pensada para que el nutricionista pueda ver de un vistazo cómo viene el día del paciente:

- Tarjeta con:
  - Total de calorías consumidas.
  - Objetivo diario (si está configurado).
  - Porcentaje de cumplimiento.
- Barra de progreso con colores:
  - Verde: dentro del rango esperado.
  - Amarillo: cerca del límite.
  - Rojo: superó el objetivo.
- Sección específica para:
  - Calorías desde alcohol, con barra de progreso y porcentaje propio.

La UI está armada con **Bootstrap 5** y **Bootstrap Icons**, buscando algo simple de leer y usar.

---

## Stack tecnológico

- Lenguaje: **Python**
- Framework web: **Django**
- Frontend: **HTML, CSS, Bootstrap 5, Bootstrap Icons**
- Base de datos: **SQLite** (por defecto de Django)
- Entorno: **venv** (entorno virtual de Python)

---

## Cómo correr el proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/nicolaslicha02/NutriTra-Proyecto-Academico-UTN.git
cd NutriTra-Proyecto-Academico-UTN


