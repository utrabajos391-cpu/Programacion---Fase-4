class ErrorSistema(Exception):
    """Excepción base para errores generales del sistema."""
    pass


class ErrorValidacion(ErrorSistema):
    """Excepción para datos inválidos o incompletos."""
    pass


class ErrorServicioNoDisponible(ErrorSistema):
    """Excepción para servicios que no están disponibles."""
    pass


class ErrorReserva(ErrorSistema):
    """Excepción para errores relacionados con reservas."""
    pass


class ErrorCalculoCosto(ErrorSistema):
    """Excepción para errores en el cálculo de costos."""
    pass