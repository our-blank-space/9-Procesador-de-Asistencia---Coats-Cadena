import os
from datetime import date, time
from src.reportes.reporte_html import GeneradorReporte

# Intentamos importar tus modelos reales del proyecto
try:
    from src.nucleo.modelos import RegistroDia
except ImportError:
    print("❌ ERROR: No se pudo importar RegistroDia desde 'src.nucleo.modelos'.")
    print("Asegúrate de ejecutar este script desde la raíz del proyecto.")
    exit(1)


def probar_generador_con_modelos_reales():
    print("⏳ Preparando datos con la estructura real de RegistroDia...")

    # Generamos registros usando tus dataclasses reales
    registros_prueba = [
        # Caso 1: Jornada normal con todos sus campos completos
        RegistroDia(
            empleado_id="FH2148",
            nombre="FH2148",
            fecha=date(2026, 6, 8),
            entrada=time(5, 57, 35),
            inicio_almuerzo=time(12, 0, 0),
            fin_almuerzo=time(13, 0, 0),
            salida=time(14, 32, 8),
            horas_trabajadas=7.97,
            tiene_novedad=False
        ),
        # Caso 2: Registro con novedad (falta salida y almuerzo)
        RegistroDia(
            empleado_id="JL1898",
            nombre="JL1898",
            fecha=date(2026, 6, 8),
            entrada=time(5, 49, 5),
            tiene_novedad=True,
            novedades=["EX-003: Sin salida final detectada"],
            # Los campos no proveídos quedarán como None gracias a tu definición del modelo
        ),
        # Caso 3: Otro empleado normal en otra fecha
        RegistroDia(
            empleado_id="AA9988",
            nombre="AA9988",
            fecha=date(2026, 6, 9),
            entrada=time(8, 0, 0),
            inicio_almuerzo=time(13, 0, 0),
            fin_almuerzo=time(14, 0, 0),
            salida=time(17, 0, 0),
            horas_trabajadas=8.0,
            tiene_novedad=False
        )
    ]

    # Carpeta de salida temporal para la prueba
    carpeta_salida = "datos/salida/prueba_reporte"

    print(f"⏳ Generando el reporte HTML en '{carpeta_salida}'...")
    try:
        # Llamar al generador
        GeneradorReporte.generar(registros_prueba, carpeta_salida)

        ruta_final = os.path.join(carpeta_salida, "reporte_grafico.html")
        if os.path.exists(ruta_final):
            print("\n✅ ¡Reporte generado con éxito con tus modelos reales!")
            print(f"Archivo creado en: {os.path.abspath(ruta_final)}")
            print("\nPara abrirlo en tu navegador, ejecuta en terminal:")
            print(f"   xdg-open {ruta_final}")
        else:
            print("\n❌ Error: El proceso finalizó pero no se localizó el reporte final.")
            
    except Exception as e:
        print(f"\n❌ Ocurrió un error inesperado al procesar el reporte: {str(e)}")


if __name__ == "__main__":
    probar_generador_con_modelos_reales()