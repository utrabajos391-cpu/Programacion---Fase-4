from abc import ABC, abstractmethod
from excepciones import ErrorValidacion, ErrorServicioNoDisponible, ErrorCalculoCosto
from logger import LoggerSistema


class Servicio(ABC):
    """
    Clase abstracta Servicio.
    Define la estructura base de todos los servicios de Software FJ.
    """

    def __init__(self, codigo, nombre, precio_base, disponible=True):
        if not codigo:
            raise ErrorValidacion("El código del servicio no puede estar vacío.")

        if not nombre or len(nombre.strip()) < 3:
            raise ErrorValidacion("El nombre del servicio debe tener mínimo 3 caracteres.")

        if precio_base <= 0:
            raise ErrorValidacion("El precio base del servicio debe ser mayor que cero.")

        self._codigo = codigo
        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = disponible

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise ErrorValidacion("La disponibilidad debe ser True o False.")
        self._disponible = estado

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{self._nombre}' no se encuentra disponible."
            )

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass


class ReservaSala(Servicio):
    """
    Servicio especializado para reserva de salas.
    """

    def __init__(self, codigo, nombre, precio_base, capacidad, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)

        if capacidad <= 0:
            raise ErrorValidacion("La capacidad de la sala debe ser mayor que cero.")

        self.__capacidad = capacidad

        LoggerSistema.registrar_evento(f"Servicio ReservaSala creado: {nombre}")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        try:
            self.validar_disponibilidad()

            if duracion <= 0:
                raise ErrorCalculoCosto("La duración debe ser mayor que cero.")

            costo = self._precio_base * duracion

            if self.__capacidad > 20:
                costo += 50000

            if descuento > 0:
                costo -= costo * descuento

            if impuesto > 0:
                costo += costo * impuesto

            return costo

        except ErrorCalculoCosto as error:
            LoggerSistema.registrar_error(f"Error calculando costo de sala: {error}")
            raise

    def describir_servicio(self):
        return (
            f"Reserva de sala: {self._nombre} | "
            f"Capacidad: {self.__capacidad} personas | "
            f"Precio base por hora: ${self._precio_base}"
        )


class AlquilerEquipo(Servicio):
    """
    Servicio especializado para alquiler de equipos tecnológicos.
    """

    def __init__(self, codigo, nombre, precio_base, tipo_equipo, garantia, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)

        if not tipo_equipo:
            raise ErrorValidacion("El tipo de equipo no puede estar vacío.")

        if garantia < 0:
            raise ErrorValidacion("El valor de la garantía no puede ser negativo.")

        self.__tipo_equipo = tipo_equipo
        self.__garantia = garantia

        LoggerSistema.registrar_evento(f"Servicio AlquilerEquipo creado: {nombre}")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        try:
            self.validar_disponibilidad()

            if duracion <= 0:
                raise ErrorCalculoCosto("La duración del alquiler debe ser mayor que cero.")

            costo = (self._precio_base * duracion) + self.__garantia

            if descuento > 0:
                costo -= costo * descuento

            if impuesto > 0:
                costo += costo * impuesto

            return costo

        except ErrorCalculoCosto as error:
            LoggerSistema.registrar_error(f"Error calculando costo de equipo: {error}")
            raise

    def describir_servicio(self):
        return (
            f"Alquiler de equipo: {self._nombre} | "
            f"Tipo: {self.__tipo_equipo} | "
            f"Garantía: ${self.__garantia} | "
            f"Precio base por hora: ${self._precio_base}"
        )


class AsesoriaEspecializada(Servicio):
    """
    Servicio especializado para asesorías profesionales.
    """

    def __init__(self, codigo, nombre, precio_base, area, asesor, disponible=True):
        super().__init__(codigo, nombre, precio_base, disponible)

        if not area:
            raise ErrorValidacion("El área de asesoría no puede estar vacía.")

        if not asesor:
            raise ErrorValidacion("El nombre del asesor no puede estar vacío.")

        self.__area = area
        self.__asesor = asesor

        LoggerSistema.registrar_evento(f"Servicio AsesoriaEspecializada creado: {nombre}")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        try:
            self.validar_disponibilidad()

            if duracion <= 0:
                raise ErrorCalculoCosto("La duración de la asesoría debe ser mayor que cero.")

            costo = self._precio_base * duracion

            if self.__area.lower() in ["programación", "programacion", "ciberseguridad", "bases de datos"]:
                costo += 80000

            if descuento > 0:
                costo -= costo * descuento

            if impuesto > 0:
                costo += costo * impuesto

            return costo

        except ErrorCalculoCosto as error:
            LoggerSistema.registrar_error(f"Error calculando costo de asesoría: {error}")
            raise

    def describir_servicio(self):
        return (
            f"Asesoría especializada: {self._nombre} | "
            f"Área: {self.__area} | "
            f"Asesor: {self.__asesor} | "
            f"Precio base por hora: ${self._precio_base}"
        )