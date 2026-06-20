from datetime import timedelta
from typing import List
from src.nucleo.modelos import Marcacion, RegistroDia
from itertools import groupby

class ProcesadorAsistencia:
    """
    El cerebro del sistema. Recibe marcaciones limpias y calcula:
    - Las horas trabajadas descontando el almuerzo.
    - Qué días tienen novedades o inconsistencias.
    """

    def procesar(self, marcaciones: List[Marcacion]) -> List[RegistroDia]:
        resultados = []

        # Paso 1: Ordenar todas las marcas por empleado y luego por fecha y hora
        marcaciones_ordenadas = sorted(
            marcaciones, key=lambda m: (m.empleado_id, m.fecha, m.hora)
        )

        # Paso 2: Agrupar por empleado + fecha (cada grupo = un día de trabajo)
        for clave, grupo in groupby(
            marcaciones_ordenadas, key=lambda m: (m.empleado_id, m.fecha)
        ):
            emp_id, fecha = clave
            marcas_del_dia = list(grupo)

            # Crear el registro del día
            registro = RegistroDia(
                empleado_id=emp_id,
                nombre=emp_id,
                fecha=fecha
            )

            # Paso 3: Eliminar marcas duplicadas (misma hora exacta)
            horas_vistas = set()
            marcas_unicas = []
            for m in marcas_del_dia:
                if m.hora not in horas_vistas:
                    horas_unicas = horas_vistas.add(m.hora)
                    marcas_unicas.append(m)
                else:
                    # EX-005: Marca duplicada detectada
                    registro.novedades.append("EX-005: Marca duplicada eliminada")
                    registro.tiene_novedad = True

            # Paso 4: Asignar marcas según su posición cronológica
            total = len(marcas_unicas)

            if total >= 1:
                registro.entrada = marcas_unicas[0].hora
            if total >= 2:
                registro.inicio_almuerzo = marcas_unicas[1].hora
            if total >= 3:
                registro.fin_almuerzo = marcas_unicas[2].hora
            if total >= 4:
                registro.salida = marcas_unicas[3].hora

            # Paso 5: Detectar novedades según cantidad de marcas
            if total < 4:
                registro.tiene_novedad = True
                if total == 0:
                    registro.novedades.append("EX-002: Sin entrada registrada")
                elif total < 4:
                    registro.novedades.append(
                        f"EX-001: Marcaciones incompletas ({total}/4)"
                    )
            if total > 4:
                registro.tiene_novedad = True
                registro.novedades.append(f"EX-006: Exceso de marcaciones ({total}/4)")

            # Paso 6: Calcular horas solo si el día está completo
            if registro.entrada and registro.inicio_almuerzo \
               and registro.fin_almuerzo and registro.salida:
                
                # Convertir horas a objetos datetime para poder restarlos
                from datetime import datetime
                base = datetime(2000, 1, 1)  # Fecha ficticia solo para calcular
                
                t_entrada        = datetime.combine(base, registro.entrada)
                t_ini_almuerzo   = datetime.combine(base, registro.inicio_almuerzo)
                t_fin_almuerzo   = datetime.combine(base, registro.fin_almuerzo)
                t_salida         = datetime.combine(base, registro.salida)

                # Fórmula: (salida - entrada) - (fin_almuerzo - inicio_almuerzo)
                tiempo_manana  = t_ini_almuerzo - t_entrada
                tiempo_tarde   = t_salida - t_fin_almuerzo
                total_segundos = (tiempo_manana + tiempo_tarde).total_seconds()

                registro.horas_trabajadas = round(total_segundos / 3600, 2)
            else:
                # Sin salida = no podemos calcular horas reales
                if total >= 1 and not registro.salida:
                    registro.novedades.append("EX-003: Sin salida final detectada")
                    registro.tiene_novedad = True
                registro.horas_trabajadas = 0.0

            resultados.append(registro)

        return resultados



"""
# ==========================================
# BLOQUE DE PRUEBA: PROCESADOR DE ASISTENCIA
# ==========================================
if __name__ == '__main__':
    from datetime import date, time
    
    print("--- Iniciando prueba del Procesador de Asistencia ---")
    

    # 1. Definimos datos de prueba ajustados a la clase Marcacion
    datos_simulados = [
        # empleado_id, nombre, fecha, hora, tipo
        Marcacion("EMP-01", "Juan Perez", date(2026, 6, 19), time(8, 0), "E"),
        Marcacion("EMP-01", "Juan Perez", date(2026, 6, 19), time(12, 0), "S"),
        Marcacion("EMP-01", "Juan Perez", date(2026, 6, 19), time(13, 0), "E"),
        Marcacion("EMP-01", "Juan Perez", date(2026, 6, 19), time(17, 0), "S"),
        
        Marcacion("EMP-02", "Ana Lopez", date(2026, 6, 19), time(8, 0), "E"),
        
        Marcacion("EMP-03", "Luis Diaz", date(2026, 6, 19), time(8, 0), "E"),
        Marcacion("EMP-03", "Luis Diaz", date(2026, 6, 19), time(8, 0), "E"),
    ]
    # 2. Ejecutamos el procesador
    procesador = ProcesadorAsistencia()
    resultados = procesador.procesar(datos_simulados)
    
    # 3. Reporte de resultados
    print(f"Total de registros generados: {len(resultados)}\n")
    
    for res in resultados:
        estado = "❌ CON NOVEDAD" if res.tiene_novedad else "✅ OK"
        print(f"Empleado: {res.empleado_id} | Horas: {res.horas_trabajadas} | Estado: {estado}")
        if res.novedades:
            print(f"   Detalles: {', '.join(res.novedades)}")
    
    print("\n--- Fin de la prueba ---")
    """