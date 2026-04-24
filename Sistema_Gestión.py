from abc import ABC, abstractmethod
from datetime import datetime


# ============================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# Empresa: Software FJ
# Curso: Programación - Fase 4
# ============================================================


# ==========================
# FUNCIÓN PARA REGISTRAR LOGS
# ==========================

def registrar_log(mensaje):
    try:
        with open("logs_sistema.txt", "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] {mensaje}\n")
    except Exception as error:
        print(f"No se pudo escribir en el archivo de logs: {error}")


# ==========================
# EXCEPCIONES PERSONALIZADAS
# ==========================

class ErrorValidacion(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class ReservaInvalidaError(Exception):
    pass


class OperacionNoPermitidaError(Exception):
    pass


# ==========================
# CLASE ABSTRACTA GENERAL
# ==========================

class EntidadSistema(ABC):
    def __init__(self, codigo):
        if not codigo:
            raise ErrorValidacion("El código de la entidad no puede estar vacío.")
        self._codigo = codigo

    @abstractmethod
    def mostrar_informacion(self):
        pass


# ==========================
# CLASE CLIENTE
# ==========================

class Cliente(EntidadSistema):
    def __init__(self, codigo, nombre, documento, correo):
        super().__init__(codigo)

        if not nombre or len(nombre.strip()) < 3:
            raise ErrorValidacion("El nombre del cliente debe tener mínimo 3 caracteres.")

        if not documento.isdigit():
            raise ErrorValidacion("El documento debe contener solo números.")

        if "@" not in correo or "." not in correo:
            raise ErrorValidacion("El correo electrónico no es válido.")

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo

    def mostrar_informacion(self):
        return f"Código: {self._codigo} | Cliente: {self.__nombre} | Documento: {self.__documento} | Correo: {self.__correo}"

    def obtener_nombre(self):
        return self.__nombre


# ==========================
# CLASE ABSTRACTA SERVICIO
# ==========================

class Servicio(EntidadSistema):
    def __init__(self, codigo, nombre, tarifa_base, disponible=True):
        super().__init__(codigo)

        if tarifa_base <= 0:
            raise ErrorValidacion("La tarifa base del servicio debe ser mayor que cero.")

        self._nombre = nombre
        self._tarifa_base = tarifa_base
        self._disponible = disponible

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    def verificar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio {self._nombre} no está disponible.")

    def mostrar_informacion(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Código: {self._codigo} | Servicio: {self._nombre} | Tarifa base: ${self._tarifa_base} | Estado: {estado}"


# ==========================
# SERVICIO 1: RESERVA DE SALA
# ==========================

class ServicioReservaSala(Servicio):
    def __init__(self, codigo, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)

        if capacidad <= 0:
            raise ErrorValidacion("La capacidad de la sala debe ser mayor que cero.")

        self.capacidad = capacidad

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorValidacion("La duración de la reserva de sala debe ser mayor que cero.")
        if duracion > 8:
            raise ErrorValidacion("La sala no se puede reservar por más de 8 horas.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._tarifa_base * duracion
        subtotal -= subtotal * descuento
        total = subtotal + subtotal * impuesto
        return total

    def describir_servicio(self):
        return f"Reserva de sala con capacidad para {self.capacidad} personas."


# ==========================
# SERVICIO 2: ALQUILER DE EQUIPO
# ==========================

class ServicioAlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, tarifa_base, tipo_equipo, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)

        if not tipo_equipo:
            raise ErrorValidacion("El tipo de equipo no puede estar vacío.")

        self.tipo_equipo = tipo_equipo

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorValidacion("La duración del alquiler debe ser mayor que cero.")
        if duracion > 30:
            raise ErrorValidacion("El equipo no se puede alquilar por más de 30 días.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._tarifa_base * duracion
        subtotal -= subtotal * descuento
        total = subtotal + subtotal * impuesto
        return total

    def describir_servicio(self):
        return f"Alquiler de equipo tipo {self.tipo_equipo}."


# ==========================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# ==========================

class ServicioAsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, tarifa_base, area, disponible=True):
        super().__init__(codigo, nombre, tarifa_base, disponible)

        if not area:
            raise ErrorValidacion("El área de asesoría no puede estar vacía.")

        self.area = area

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise ErrorValidacion("La duración de la asesoría debe ser mayor que cero.")
        if duracion > 12:
            raise ErrorValidacion("La asesoría no puede superar 12 horas.")

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        self.validar_parametros(duracion)
        subtotal = self._tarifa_base * duracion
        subtotal -= subtotal * descuento
        total = subtotal + subtotal * impuesto
        return total

    def describir_servicio(self):
        return f"Asesoría especializada en el área de {self.area}."


# ==========================
# CLASE RESERVA
# ==========================

class Reserva:
    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente asociado a la reserva no es válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio asociado a la reserva no es válido.")

        servicio.verificar_disponibilidad()
        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Creada"

    def confirmar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("No se puede confirmar una reserva cancelada.")

        self.estado = "Confirmada"
        registrar_log(f"Reserva confirmada para el cliente {self.cliente.obtener_nombre()}.")

    def cancelar(self):
        if self.estado == "Procesada":
            raise OperacionNoPermitidaError("No se puede cancelar una reserva ya procesada.")

        self.estado = "Cancelada"
        registrar_log(f"Reserva cancelada para el cliente {self.cliente.obtener_nombre()}.")

    def procesar(self):
        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas.")

        costo = self.servicio.calcular_costo(self.duracion, descuento=0.05, impuesto=0.19)
        self.estado = "Procesada"
        registrar_log(f"Reserva procesada para {self.cliente.obtener_nombre()}. Total: ${costo:.2f}")
        return costo

    def mostrar_reserva(self):
        return f"Cliente: {self.cliente.obtener_nombre()} | Servicio: {self.servicio._nombre} | Duración: {self.duracion} | Estado: {self.estado}"


# ==========================
# SIMULACIÓN DE OPERACIONES
# ==========================

def ejecutar_operacion(numero, descripcion, funcion):
    print(f"\nOPERACIÓN {numero}: {descripcion}")
    try:
        resultado = funcion()
    except ErrorValidacion as error:
        print(f"Error de validación: {error}")
        registrar_log(f"ERROR VALIDACIÓN - Operación {numero}: {error}")
    except ServicioNoDisponibleError as error:
        print(f"Servicio no disponible: {error}")
        registrar_log(f"SERVICIO NO DISPONIBLE - Operación {numero}: {error}")
    except ReservaInvalidaError as error:
        print(f"Reserva inválida: {error}")
        registrar_log(f"RESERVA INVÁLIDA - Operación {numero}: {error}")
    except OperacionNoPermitidaError as error:
        print(f"Operación no permitida: {error}")
        registrar_log(f"OPERACIÓN NO PERMITIDA - Operación {numero}: {error}")
    except Exception as error:
        print(f"Error inesperado: {error}")
        registrar_log(f"ERROR INESPERADO - Operación {numero}: {error}")
    else:
        if resultado is not None:
            print(resultado)
        registrar_log(f"Operación {numero} ejecutada correctamente.")
    finally:
        print("La operación finalizó y el sistema continúa activo.")


# ==========================
# PROGRAMA PRINCIPAL
# ==========================

def main():
    print("==============================================")
    print(" SISTEMA INTEGRAL SOFTWARE FJ")
    print(" Gestión de clientes, servicios y reservas")
    print("==============================================")

    clientes = []
    servicios = []
    reservas = []

    ejecutar_operacion(1, "Registro válido de cliente", lambda: clientes.append(
        Cliente("C001", "Juan Pérez", "1020304050", "juanperez@gmail.com")
    ) or clientes[-1].mostrar_informacion())

    ejecutar_operacion(2, "Registro inválido de cliente con documento incorrecto", lambda: clientes.append(
        Cliente("C002", "Ana Gómez", "ABC123", "ana@gmail.com")
    ))

    ejecutar_operacion(3, "Registro inválido de cliente con correo incorrecto", lambda: clientes.append(
        Cliente("C003", "Luis Torres", "1098765432", "luiscorreo.com")
    ))

    ejecutar_operacion(4, "Creación válida de servicio de reserva de sala", lambda: servicios.append(
        ServicioReservaSala("S001", "Sala ejecutiva", 50000, 20)
    ) or servicios[-1].mostrar_informacion())

    ejecutar_operacion(5, "Creación válida de servicio de alquiler de equipo", lambda: servicios.append(
        ServicioAlquilerEquipo("S002", "Alquiler de portátil", 30000, "Computador portátil")
    ) or servicios[-1].mostrar_informacion())

    ejecutar_operacion(6, "Creación válida de servicio de asesoría especializada", lambda: servicios.append(
        ServicioAsesoriaEspecializada("S003", "Asesoría en software", 80000, "Desarrollo de aplicaciones")
    ) or servicios[-1].mostrar_informacion())

    ejecutar_operacion(7, "Creación incorrecta de servicio con tarifa negativa", lambda: servicios.append(
        ServicioReservaSala("S004", "Sala pequeña", -20000, 10)
    ))

    ejecutar_operacion(8, "Reserva exitosa de sala", lambda: reservas.append(
        Reserva(clientes[0], servicios[0], 3)
    ) or reservas[-1].mostrar_reserva())

    ejecutar_operacion(9, "Reserva fallida por duración inválida", lambda: reservas.append(
        Reserva(clientes[0], servicios[0], 10)
    ))

    ejecutar_operacion(10, "Confirmación de reserva válida", lambda: reservas[0].confirmar() or reservas[0].mostrar_reserva())

    ejecutar_operacion(11, "Procesamiento de reserva confirmada", lambda: f"Total a pagar: ${reservas[0].procesar():.2f}")

    ejecutar_operacion(12, "Intento de cancelar una reserva ya procesada", lambda: reservas[0].cancelar())

    ejecutar_operacion(13, "Servicio no disponible", lambda: reservas.append(
        Reserva(clientes[0], ServicioAlquilerEquipo("S005", "Proyector", 25000, "Video beam", disponible=False), 2)
    ))

    print("\n==============================================")
    print(" SIMULACIÓN FINALIZADA")
    print(" Revise el archivo logs_sistema.txt")
    print("==============================================")


if __name__ == "__main__":
    main()