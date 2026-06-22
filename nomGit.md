Para llevar un control profesional de tu proyecto, lo ideal es seguir la convención de **Conventional Commits**. Aquí tienes la guía estructurada en formato Markdown para que puedas consultarla siempre que lo necesites.

---

# Guía de Nomenclatura de Commits

El formato estándar es:
`tipo(alcance): descripción`

## 1. Estructura del mensaje

* **tipo**: Define la naturaleza del cambio.
* **alcance (opcional)**: El módulo o archivo específico que fue modificado (ej: `procesador`, `modelos`, `main`).
* **descripción**: Un resumen breve y claro del cambio (usar imperativo: "añadir", "corregir", "mejorar").

---

## 2. Tipos de Commits

| Tipo | Descripción |
| --- | --- |
| `feat` | **Nueva funcionalidad** para el usuario. |
| `fix` | **Corrección de un error** (*bug*). |
| `docs` | Cambios en documentación (README, comentarios). |
| `refactor` | Cambio de código que no añade funciones ni corrige errores. |
| `style` | Cambios de formato (espacios, comas, indentación) que no afectan la lógica. |
| `test` | Añadir o modificar pruebas unitarias. |
| `chore` | Tareas de mantenimiento, configuración o dependencias. |

---

## 3. Ejemplos Prácticos

Aquí tienes ejemplos aplicados a tu proyecto de **Procesador de Asistencia**:

### Funcionalidades y Errores

* `feat(procesador): añadir normalización de minutos en duplicados`
* `fix(procesador): corregir la posición de la lógica de duplicados`
* `fix(test): solucionar error en módulo de importación al ejecutar con -m`

### Mantenimiento y Documentación

* `docs(readme): explicar la lógica de los 4 registros clave`
* `refactor(procesador): simplificar la resta de horas mediante datetime`
* `style(procesador): corregir indentación y espacios en blanco`
* `chore(git): añadir archivo .gitignore para entorno virtual`

---

## 4. Reglas de Oro

1. **Imperativo y presente**: Escribe como si estuvieras dando una orden al código (*"Añadir soporte para..."* en lugar de *"Añadí soporte para..."*).
2. **Brevedad**: Intenta que la descripción no supere los 50 caracteres.
3. **Atomicidad**: Haz commits pequeños. Es mejor tener tres commits que expliquen cambios específicos que uno gigante que diga "todo cambiado".
4. **Separación de conceptos**: Si arreglaste un error y además cambiaste la documentación, haz **dos commits distintos**.

---

¿Te gustaría que generáramos un pequeño archivo `CONTRIBUTING.md` para que cualquier persona que colabore en tu proyecto sepa cómo nombrar sus cambios?