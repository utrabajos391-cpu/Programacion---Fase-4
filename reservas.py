from excepciones import ErrorReserva, ErrorValidacion, ErrorServicioNoDisponible
from logger import LoggerSistema


class Reserva:
    """
    Clase Reserva que integra cliente, servicio, duración y estado.
    """

    ESTADOS_VALIDOS = ["Pendiente", "Confirmada", "Cancelada", "Procesada"]

    def __init__(self, codigo, cliente, servicio, duracion):
        if not codigo:
            raise ErrorValidacion("El código de la reserva no puede estar vacío.")

        if cliente is None:
            raise ErrorValidacion("La reserva debe tener un cliente asociado.")

        if servicio is None:
            raise ErrorValidacion("La reserva debe tener un servicio asociado.")

        if duracion <= 0:
            raise ErrorValidacion("La duración de la reserva debe ser mayor que cero.")

        self.__codigo = codigo
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = "Pendiente"
        self.__costo_total = 0

        LoggerSistema.registrar_evento(f"Reserva creada correctamente: {self.__codigo}")

    @property
    def codigo(self):
        return self.__codigo

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def confirmar(self):
        """
        Confirma una reserva si está en estado pendiente.
        """
        try:
            if self.__estado != "Pendiente":
                raise ErrorReserva(
                    f"No se puede confirmar una reserva en estado {self.__estado}."
                )

            self.__servicio.validar_disponibilidad()
            self.__estado = "Confirmada"

        except ErrorServicioNoDisponible as error:
            LoggerSistema.registrar_error(f"No se pudo confirmar la reserva: {error}")
            raise ErrorReserva("La reserva no pudo confirmarse porque el servicio no está disponible.") from error

        except ErrorReserva as error:
            LoggerSistema.registrar_error(str(error))
            raise

        else:
            LoggerSistema.registrar_evento(f"Reserva confirmada: {self.__codigo}")
            print(f"Reserva {self.__codigo} confirmada correctamente.")

        finally:
            LoggerSistema.registrar_evento(
                f"Finalizó el intento de confirmación de la reserva {self.__codigo}"
            )

    def cancelar(self):
        """
        Cancela una reserva siempre que no esté procesada.
        """
        try:
            if self.__estado == "Procesada":
                raise ErrorReserva("No se puede cancelar una reserva ya procesada.")

            if self.__estado == "Cancelada":
                raise ErrorReserva("La reserva ya se encuentra cancelada.")

            self.__estado = "Cancelada"

        except ErrorReserva as error:
            LoggerSistema.registrar_error(f"Error cancelando reserva: {error}")
            raise

        else:
            LoggerSistema.registrar_evento(f"Reserva cancelada: {self.__codigo}")
            print(f"Reserva {self.__codigo} cancelada correctamente.")

        finally:
            LoggerSistema.registrar_evento(
                f"Finalizó el intento de cancelación de la reserva {self.__codigo}"
            )

    def procesar(self, descuento=0, impuesto=0):
        """
        Procesa una reserva confirmada y calcula su costo total.
        """
        try:
            if self.__estado != "Confirmada":
                raise ErrorReserva(
                    "Solo se pueden procesar reservas confirmadas."
                )

            self.__costo_total = self.__servicio.calcular_costo(
                self.__duracion,
                descuento,
                impuesto
            )

            self.__estado = "Procesada"

        except Exception as error:
            LoggerSistema.registrar_error(f"Error procesando reserva {self.__codigo}: {error}")
            raise ErrorReserva("No fue posible procesar la reserva correctamente.") from error

        else:
            LoggerSistema.registrar_evento(
                f"Reserva procesada: {self.__codigo} | Costo total: {self.__costo_total}"
            )
            print(f"Reserva {self.__codigo} procesada correctamente.")
            print(f"Costo total: ${self.__costo_total:,.0f}")

        finally:
            LoggerSistema.registrar_evento(
                f"Finalizó el procesamiento de la reserva {self.__codigo}"
            )

    def mostrar_reserva(self):
        return (
            f"Reserva: {self.__codigo} | "
            f"Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | "
            f"Duración: {self.__duracion} horas | "
            f"Estado: {self.__estado} | "
            f"Costo total: ${self.__costo_total:,.0f}"
        )