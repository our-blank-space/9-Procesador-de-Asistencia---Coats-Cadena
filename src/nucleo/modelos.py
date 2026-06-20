from dataclasses import dataclass, field
from datetime import date, time
from typing import Optional, List

@dataclass
class Marcacion:
    empleado_id: str
    nombre: str
    fecha: date
    hora: time
    tipo: str  

@dataclass
class RegistroDia:
    empleado_id: str
    nombre: str
    fecha: date
    entrada: Optional[time] = None
    inicio_almuerzo: Optional[time] = None
    fin_almuerzo: Optional[time] = None
    salida: Optional[time] = None
    horas_trabajadas: Optional[float] = None
    tiene_novedad: bool = False
    novedades: List[str] = field(default_factory=list)
