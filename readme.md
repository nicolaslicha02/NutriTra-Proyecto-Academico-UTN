# NutriTra  
_Plataforma de seguimiento nutricional entre pacientes y nutricionistas_

**NutriTra** es una aplicación web desarrollada con **Django** que funciona como un **nexo digital entre nutricionistas y pacientes**.  
Permite registrar ingestas diarias, calcular calorías consumidas y mostrar un resumen visual que el profesional puede usar durante la consulta.

> Proyecto académico desarrollado por estudiantes de la **UTN – Facultad Regional La Plata**.

---

##  ¿Qué resuelve NutriTra?

En una consulta tradicional, el nutricionista pregunta “¿cómo venís comiendo estos días?” y el paciente responde de memoria.  
**NutriTra** busca reemplazar ese “a ojo” por datos:

- El nutricionista puede:
  - Registrar pacientes.
  - Cargar sus ingestas diarias.
  - Ver un resumen claro del día (calorías y porcentajes).
- El paciente, indirectamente, termina teniendo un registro más ordenado de lo que consume.

---

##  Funcionalidades principales (versión actual)

###  Gestión de pacientes

- ABM (Alta, Baja, Modificación) de **pacientes**.
- Datos básicos de identificación.
- Pensado para que cada nutricionista tenga su cartera de pacientes organizada.

###  Registro de ingestas

Para cada paciente y para cada día se pueden registrar ingestas:

- Descripción del alimento/bebida.
- Cantidad / porción.
- Calorías estimadas.
- Opción para marcar si la ingesta aporta **calorías desde alcohol**.

A partir de esto, el sistema calcula:

-  **Calorías totales del día.**  
-  **Porcentaje respecto al objetivo diario estimado.**  
-  **Porcentaje de calorías que provienen del alcohol.**

###  Dashboard diario

Pantalla pensada para que el nutricionista pueda ver “de un vistazo” cómo viene el día del paciente:

- Tarjeta con:
  - Total de calorías consumidas.
  - Objetivo diario de calorías (si está configurado).
  - Porcentaje de cumplimiento.
- Barra de progreso con colores:
  - **Verde:** dentro del rango esperado.
  - **Amarillo:** cerca del límite.
  - **Rojo:** superó el objetivo.
- Sección específica:
  - **Calorías desde alcohol** + barra de progreso y porcentaje.

La UI está construida con **Bootstrap 5** y **Bootstrap Icons**, buscando una interfaz simple y clara.

---

##  Stack tecnológico

- **Lenguaje:** Python
- **Framework web:** Django
- **Frontend:** HTML, CSS, Bootstrap 5, Bootstrap Icons
- **Base de datos:** SQLite (default de Django)
- **Entorno:** `venv` (entorno virtual de Python)

---

##  Cómo correr el proyecto 

### 1. Clonar el repositorio

```bash
git clone https://github.com/nicolaslicha02/NutriTra-Proyecto-Academico-UTN.git
cd NutriTra-Proyecto-Academico-UTN

