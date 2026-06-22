# ⏱️ Procesador de Asistencia - Coats Cadena

**Postulación: Práctica Profesional — Coats Cadena**  
**Tecnología Principal:** Python 3.11+ | **Visualización:** Plotly + HTML  
**Control de versiones:** Git

# Enfoque

Este proyecto es una herramienta automatizada para procesar los registros de ingreso y salida de los empleados, desarrollada como parte de la prueba técnica para realizar la práctica profesional en Coats Cadena.

## 🚀 Características Principales
- **Lectura Automática**: Procesa archivos Excel con marcaciones de empleados de forma robusta.
- **Cálculo Preciso**: Calcula horas trabajadas descontando los tiempos destinados a la alimentación.
- **Detección de Inconsistencias**: Identifica y reporta marcaciones incompletas, duplicadas, faltas de ingreso/salida y otras anomalías (8 tipos de reglas de validación).
- **Interfaz Gráfica Amigable (GUI)**: Pantalla moderna y fácil de usar para cargar datos y visualizar el proceso sin tocar código.
- **Reportes Visuales Interactivos**: Genera reportes interactivos en HTML usando la librería Plotly.
- **Exportación Limpia**: Crea automáticamente archivos Excel de resumen y un registro detallado de las novedades encontradas.


## 🛠️ Requisitos del Sistema
Para poder ejecutar esta aplicación, necesitas tener instalado:
- **Python 3.11** o superior.

## 📦 Instrucciones de Instalación
Sigue estos pasos para configurar el proyecto en tu computadora:

1. Abre la terminal en la carpeta del proyecto (`procesador-asistencia`).

2. **Crear un entorno virtual** (muy recomendado para mantener ordenadas las librerías):
   ```bash
   python -m venv venv
   ```
3. **Activar el entorno virtual**:
   - En Windows: `venv\Scripts\activate`
   - En Linux/Mac: `source venv/bin/activate`

4. **Instalar las dependencias necesarias**:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecucion en modo desarrollo Interfaz Gráfica 
Ejecuta este comando en la terminal:
```bash
python principal.py
```
Se abrirá una ventana donde podrás hacer clic en "Cargar Archivo Excel", procesar la información con un solo botón y ver los resultados directamente en la pantalla, además de exportarlos.

## 📁 Estructura del Proyecto
- `src/` (Código fuente): Contiene toda la lógica pura. Aquí hacemos las validaciones, los cálculos y la lectura de los Excel. Todo separado ordenadamente.
- `datos/`: Carpeta destinada a guardar los archivos Excel
- (`entrada/`) y los resultados generados (`salida/`).
- `pruebas/`: Código de pruebas automatizadas para asegurar matemáticamente que nuestros cálculos de horas nunca fallan.

## Ejecutar pruebas unitarias
pytest test/test_app_gui.py
pytest /home/compartido/Desarrollo/procesador-asistencia/test

## Empaquetado 
### Herramienta de empaquetado
- pip install pyinstaller

- pyinstaller --onefile main.py

## 6. Respuesta a la Pregunta Complementaria

### ¿Qué procesos de una tintorería industrial considera que podrían beneficiarse de la automatización mediante herramientas de software?

Fundamentalme la automatización hace un papel crucial para una tintoreria industrial ¿Porque?.

Inicilmente evaluar cada uno de los procesos con la adquicicion de datos para hacer implementaciones de software en las siguientes areas

1. **Preparación y Pretratamiento**

Para esta area se puede tener encuenta un sofware atematizado para el tema de inventario, para gestionar y evaluar los recurso, ademas usando integraciones con Inteligencia artificial con la herramienta **n8n** por si misma puede genorar reportes cosolidados para los pedidos del siguiente mes y tener una trasabilidad clara de cuanto es su inversion de cada producto bruto. para una mejora en la toma de decicion futura.

2. **Tintura**

Este es un paso que define el color estandar de una fibra, por lo tanto saber la docificacion de cada quimico u o recurso que afecta directa o indirectamente su color. es claramente fundamental para que el teñido del día de hoy sea igual al del día siguiente. Esto es más una integracion con el desarrollo en mecatronica, para usar elementos como sensores u o inyección automatizadas de un quimico en especifico para estandarizar este proceso y no allá errores humanos. 

3. Post-tratamiento

En este sector encontramos ares de maquinas de lavado, suavisante y secado, cada una de estas ares es claramente fundametal medir y gestionar cada uno de estos recurso y automatizar el analisis de los mismos utilizando herramientas como **QUARTO** o **R**, para informes claros, teniendo encuenta que ya hay herramientas de mecatronica ya implementadas. Para su debido analisis para posibles mejoras en cada uno de esos procesos.




