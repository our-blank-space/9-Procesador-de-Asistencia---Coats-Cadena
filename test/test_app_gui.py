import unittest
from unittest.mock import MagicMock, patch
import customtkinter as ctk

from src.interfaz.app import AplicacionGUI


class TestAplicacionGUI(unittest.TestCase):

    def setUp(self):
        """Inicializa la interfaz antes de cada prueba sin mostrarla."""
        self.app = AplicacionGUI()
        self.app.withdraw()

    def tearDown(self):
        """Libera correctamente los recursos de la GUI."""
        try:
            if self.app.winfo_exists():
                self.app.update_idletasks()
                self.app.destroy()
        except:
            pass

    def test_inicializacion_por_defecto(self):
        """Verifica el estado inicial."""
        self.assertIsNone(self.app.ruta_archivo)
        self.assertEqual(self.app.registros, [])
        self.assertIsNone(self.app._carpeta_salida)
        self.assertEqual(self.app._resumen_datos, {})

        self.assertEqual(self.app.btn_procesar.cget("state"), "disabled")
        self.assertEqual(self.app.btn_excel.cget("state"), "disabled")
        self.assertEqual(self.app.btn_html.cget("state"), "disabled")

    def test_en_archivo_listo_habilita_boton(self):
        """Verifica que seleccionar archivo habilite procesar."""
        ruta_ficticia = "/ruta/al/archivo/asistencia.xlsx"
        self.app._en_archivo_listo(ruta_ficticia)

        self.assertEqual(self.app.ruta_archivo, ruta_ficticia)
        self.assertEqual(self.app.btn_procesar.cget("state"), "normal")

    @patch('src.interfaz.app.threading.Thread')
    @patch('src.interfaz.app.LectorExcel')
    @patch('src.interfaz.app.ProcesadorAsistencia')
    @patch('src.interfaz.app.EscritorExcel')
    @patch('src.interfaz.app.GeneradorReporte')
    def test_procesamiento_exitoso(
        self,
        mock_generador,
        mock_escritor,
        mock_procesador,
        mock_lector,
        mock_thread
    ):
        """Prueba flujo exitoso."""

        # Ejecutar la función objetivo del hilo inmediatamente
        def ejecutar_sincronamente(*args, **kwargs):
            target = kwargs.get('target')
            if target:
                target()  # Ejecuta app._procesar()
            return MagicMock()

        mock_thread.side_effect = ejecutar_sincronamente

        # Datos simulados
        mock_lector.leer_marcaciones.return_value = ["marcacion1", "marcacion2"]

        registro_mock = MagicMock()
        registro_mock.empleado_id = "EMP001"
        registro_mock.horas_trabajadas = 8.0
        registro_mock.tiene_novedad = False

        procesador_instancia = MagicMock()
        procesador_instancia.procesar.return_value = [registro_mock]
        mock_procesador.return_value = procesador_instancia

        self.app.ruta_archivo = "/test/asistencia.xlsx"
        self.app._iniciar_procesamiento()

        mock_lector.leer_marcaciones.assert_called_once_with("/test/asistencia.xlsx")
        procesador_instancia.procesar.assert_called_once_with(["marcacion1", "marcacion2"])
        mock_escritor.generar_reportes.assert_called_once()
        mock_generador.generar.assert_called_once()

        self.assertEqual(self.app._resumen_datos["empleados"], 1)
        self.assertEqual(self.app._resumen_datos["horas"], 8.0)
        self.assertEqual(self.app._resumen_datos["novedades"], 0)
        self.assertEqual(self.app.btn_excel.cget("state"), "normal")
        self.assertEqual(self.app.btn_html.cget("state"), "normal")

    @patch('src.interfaz.app.threading.Thread')
    @patch('src.interfaz.app.LectorExcel')
    @patch('src.interfaz.app.messagebox.showerror')
    def test_procesamiento_con_error(
        self,
        mock_showerror,
        mock_lector,
        mock_thread
    ):
        """Verifica captura de errores."""

        # Ejecutar la función objetivo del hilo inmediatamente
        def ejecutar_sincronamente(*args, **kwargs):
            target = kwargs.get('target')
            if target:
                target()
            return MagicMock()

        mock_thread.side_effect = ejecutar_sincronamente

        mock_lector.leer_marcaciones.side_effect = Exception("Formato inválido")

        self.app.ruta_archivo = "/test/asistencia.xlsx"
        self.app._iniciar_procesamiento()

        mock_showerror.assert_called_once_with("Error", "Formato inválido")
        self.assertEqual(self.app.btn_procesar.cget("state"), "normal")

    @patch('src.interfaz.app.webbrowser.open')
    @patch('src.interfaz.app.os.path.exists')
    @patch('src.interfaz.app.messagebox.showwarning')
    def test_abrir_navegador_sin_archivo(
        self,
        mock_showwarning,
        mock_exists,
        mock_webbrowser_open
    ):
        """Verifica aviso cuando el HTML no existe."""
        self.app._carpeta_salida = "/test/salida"
        mock_exists.return_value = False

        self.app._abrir_navegador()

        mock_webbrowser_open.assert_not_called()
        mock_showwarning.assert_called_once_with(
            "Aviso",
            "No se encontró el archivo 'reporte_grafico.html' en la carpeta de resultados."
        )


if __name__ == '__main__':
    unittest.main()
