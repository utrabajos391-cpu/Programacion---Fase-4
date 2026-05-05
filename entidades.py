from abc import ABC, abstractmethod
from excepciones import ErrorValidacion
from logger import LoggerSistema


class EntidadSistema(ABC):
    """
    Clase abstracta general para representar entidades del sistema.
    """

    def __init__(self, identificador):
        if not identificador:
            raise ErrorValidacion("El identificador no puede estar vacío.")
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self):
        pass


class Cliente(EntidadSistema):
    """
    Clase Cliente con encapsulación y validaciones robustas.
    """

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        self.__nombre = None
        self.__correo = None
        self.__telefono = None

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        LoggerSistema.registrar_evento(
            f"Cliente creado correctamente: {self.__nombre}"
        )

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ErrorValidacion("El nombre del cliente debe tener mínimo 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor:
            raise ErrorValidacion("El correo electrónico no tiene un formato válido.")
        self.__correo = valor.strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not str(valor).isdigit() or len(str(valor)) < 7:
            raise ErrorValidacion("El teléfono debe contener solo números y mínimo 7 dígitos.")
        self.__telefono = str(valor)

    def mostrar_informacion(self):
        return (
            f"Cliente ID: {self.identificador} | "
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )