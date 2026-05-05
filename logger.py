from datetime import datetime


class LoggerSistema:
    """
    Clase encargada de registrar eventos y errores del sistema
    en un archivo de logs.
    """

    ARCHIVO_LOG = "eventos.log"

    @staticmethod
    def registrar_evento(mensaje):
        """
        Registra eventos informativos del sistema.
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LoggerSistema.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[EVENTO] {fecha} - {mensaje}\n")

    @staticmethod
    def registrar_error(mensaje):
        """
        Registra errores ocurridos durante la ejecución.
        """
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LoggerSistema.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[ERROR] {fecha} - {mensaje}\n")