import pandas as pd
from typing import List
from src.nucleo.modelos import Marcacion

class LectorExcel:
    """
    Se encarga únicamente de abrir el archivo Excel y convertir las filas
    en objetos 'Marcacion' para que el Cerebro las pueda entender.
    """
    @staticmethod
    def leer_marcaciones(ruta_archivo: str) -> List[Marcacion]:
        # Leer el archivo (Soporta .xlsx y el formato antiguo .xls)
        df = pd.read_excel(ruta_archivo)
        
        marcaciones = []
        # Iterar sobre cada fila del Excel original de Coats Cadena
        for _, fila in df.iterrows():
            try:
                # Extraer el ID
                emp_id = str(fila.get('ID', ''))
                if emp_id == "nan" or emp_id.strip() == "": 
                    continue # Saltar filas vacías
                
                # Convertir la fecha
                fecha_val = pd.to_datetime(str(fila.get('fecha', ''))).date()
                
                # En el Excel real, las horas vienen juntas separadas por punto y coma (;)
                horas_juntas = str(fila.get('Hora de Registro', ''))
                if horas_juntas == "nan" or horas_juntas.strip() == "":
                    continue
                
                # Separar las horas usando el punto y coma
                lista_horas_texto = horas_juntas.split(';')
                
                # Por cada hora encontrada, creamos un registro individual
                for hora_texto in lista_horas_texto:
                    hora_texto = hora_texto.strip()
                    if not hora_texto: 
                        continue
                        
                    hora_val = pd.to_datetime(hora_texto).time()
                        
                    # Crear el molde de la marcación
                    m = Marcacion(
                        empleado_id=emp_id,
                        nombre=emp_id, # El Excel no trae Nombre, usamos el ID
                        fecha=fecha_val,
                        hora=hora_val,
                        tipo="DESCONOCIDO" 
                    )
                    marcaciones.append(m)
            except Exception:
                # Si una fila está rota o tiene texto raro, la ignoramos
                pass
                
        return marcaciones


"""

# ==========================================
# BLOQUE DE PRUEBA INDIVIDUAL
# ==========================================
if __name__ == '__main__':
    print("Iniciando prueba del Lector de Excel...")
    
    # Asumiendo que tu archivo Data.xls está un nivel afuera de tu proyecto
    # Cámbialo si tu archivo está en otra ruta.
    ruta_prueba = "Data.xls" 
    
    try:
        marcas_extraidas = LectorExcel.leer_marcaciones(ruta_prueba)
        print(f"¡Éxito! Logré extraer {len(marcas_extraidas)} marcaciones individuales.")
        
        print("\nMostrando cómo se ven las primeras 3 marcaciones:")
        for marca in marcas_extraidas[:3]:
            print(marca)
            
    except Exception as e:
        print(f"Uy, algo falló: {e}")

"""