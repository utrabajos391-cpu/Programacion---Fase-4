from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reservas import Reserva
from excepciones import ErrorSistema
from logger import LoggerSistema


clientes = []
servicios = []
reservas = []


def ejecutar_operacion(numero, descripcion, funcion):
    """
    Ejecuta una operación controlada del sistema.
    Permite que el programa continúe funcionando aunque ocurra un error.
    """
    print("\n" + "=" * 70)
    print(f"OPERACIÓN {numero}: {descripcion}")
    print("=" * 70)

    try:
        funcion()

    except ErrorSistema as error:
        print(f"Error controlado del sistema: {error}")
        LoggerSistema.registrar_error(f"Operación {numero} fallida: {error}")

    except Exception as error:
        print(f"Error inesperado: {error}")
        LoggerSistema.registrar_error(f"Operación {numero} con error inesperado: {error}")

    else:
        print("Operación ejecutada correctamente.")
        LoggerSistema.registrar_evento(f"Operación {numero} ejecutada correctamente.")

    finally:
        print("Fin de la operación.")
        LoggerSistema.registrar_evento(f"Finalizó la operación {numero}.")


def operacion_1():
    cliente = Cliente("C001", "Carlos Pérez", "carlos@correo.com", "3124567890")
    clientes.append(cliente)
    print(cliente.mostrar_informacion())


def operacion_2():
    cliente = Cliente("C002", "Ana Rodríguez", "ana@correo.com", "3009876543")
    clientes.append(cliente)
    print(cliente.mostrar_informacion())


def operacion_3():
    cliente = Cliente("C003", "Lu", "lucorreo.com", "abc123")
    clientes.append(cliente)
    print(cliente.mostrar_informacion())


def operacion_4():
    servicio = ReservaSala(
        codigo="S001",
        nombre="Sala Ejecutiva",
        precio_base=70000,
        capacidad=15
    )
    servicios.append(servicio)
    print(servicio.describir_servicio())


def operacion_5():
    servicio = ReservaSala(
        codigo="S002",
        nombre="Sala Empresarial Grande",
        precio_base=120000,
        capacidad=35
    )
    servicios.append(servicio)
    print(servicio.describir_servicio())


def operacion_6():
    servicio = AlquilerEquipo(
        codigo="S003",
        nombre="Alquiler de Video Beam",
        precio_base=50000,
        tipo_equipo="Video Beam",
        garantia=100000
    )
    servicios.append(servicio)
    print(servicio.describir_servicio())


def operacion_7():
    servicio = AsesoriaEspecializada(
        codigo="S004",
        nombre="Asesoría en Programación",
        precio_base=90000,
        area="Programación",
        asesor="Ingeniero Luis Gómez"
    )
    servicios.append(servicio)
    print(servicio.describir_servicio())


def operacion_8():
    servicio = AlquilerEquipo(
        codigo="S005",
        nombre="PC",
        precio_base=-50000,
        tipo_equipo="Computador portátil",
        garantia=50000
    )
    servicios.append(servicio)
    print(servicio.describir_servicio())


def operacion_9():
    reserva = Reserva(
        codigo="R001",
        cliente=clientes[0],
        servicio=servicios[0],
        duracion=3
    )
    reservas.append(reserva)
    print(reserva.mostrar_reserva())


def operacion_10():
    reserva = reservas[0]
    reserva.confirmar()
    print(reserva.mostrar_reserva())


def operacion_11():
    reserva = reservas[0]
    reserva.procesar(descuento=0.10, impuesto=0.19)
    print(reserva.mostrar_reserva())


def operacion_12():
    reserva = Reserva(
        codigo="R002",
        cliente=clientes[1],
        servicio=servicios[1],
        duracion=2
    )
    reservas.append(reserva)
    reserva.confirmar()
    reserva.cancelar()
    print(reserva.mostrar_reserva())


def operacion_13():
    reserva = Reserva(
        codigo="R003",
        cliente=clientes[1],
        servicio=servicios[2],
        duracion=-4
    )
    reservas.append(reserva)
    print(reserva.mostrar_reserva())


def operacion_14():
    servicio_no_disponible = servicios[3]
    servicio_no_disponible.cambiar_disponibilidad(False)

    reserva = Reserva(
        codigo="R004",
        cliente=clientes[0],
        servicio=servicio_no_disponible,
        duracion=2
    )

    reservas.append(reserva)
    reserva.confirmar()
    print(reserva.mostrar_reserva())


def operacion_15():
    reserva = Reserva(
        codigo="R005",
        cliente=clientes[1],
        servicio=servicios[2],
        duracion=4
    )

    reservas.append(reserva)

    # Se intenta procesar sin confirmar primero.
    reserva.procesar()
    print(reserva.mostrar_reserva())


def mostrar_resumen_final():
    print("\n" + "#" * 70)
    print("RESUMEN FINAL DEL SISTEMA SOFTWARE FJ")
    print("#" * 70)

    print("\nCLIENTES REGISTRADOS:")
    for cliente in clientes:
        print(cliente.mostrar_informacion())

    print("\nSERVICIOS REGISTRADOS:")
    for servicio in servicios:
        print(servicio.describir_servicio())

    print("\nRESERVAS REGISTRADAS:")
    for reserva in reservas:
        print(reserva.mostrar_reserva())

    print("\nRevise el archivo 'eventos.log' para ver el registro de eventos y errores.")


def main():
    print("SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("Empresa: Software FJ")
    print("Curso: Programación - Fase 4")
    print("Aplicación orientada a objetos sin base de datos")

    LoggerSistema.registrar_evento("Inicio de ejecución del sistema Software FJ.")

    ejecutar_operacion(1, "Registro válido de cliente Carlos Pérez", operacion_1)
    ejecutar_operacion(2, "Registro válido de cliente Ana Rodríguez", operacion_2)
    ejecutar_operacion(3, "Registro inválido de cliente", operacion_3)
    ejecutar_operacion(4, "Creación correcta de servicio Reserva de Sala", operacion_4)
    ejecutar_operacion(5, "Creación correcta de sala grande", operacion_5)
    ejecutar_operacion(6, "Creación correcta de servicio Alquiler de Equipo", operacion_6)
    ejecutar_operacion(7, "Creación correcta de servicio Asesoría Especializada", operacion_7)
    ejecutar_operacion(8, "Creación incorrecta de servicio con precio negativo", operacion_8)
    ejecutar_operacion(9, "Creación correcta de reserva", operacion_9)
    ejecutar_operacion(10, "Confirmación correcta de reserva", operacion_10)
    ejecutar_operacion(11, "Procesamiento correcto con descuento e impuesto", operacion_11)
    ejecutar_operacion(12, "Reserva confirmada y cancelada correctamente", operacion_12)
    ejecutar_operacion(13, "Creación incorrecta de reserva con duración negativa", operacion_13)
    ejecutar_operacion(14, "Intento de reserva con servicio no disponible", operacion_14)
    ejecutar_operacion(15, "Intento de procesar reserva sin confirmar", operacion_15)

    mostrar_resumen_final()

    LoggerSistema.registrar_evento("Finalizó la ejecución del sistema Software FJ.")


if __name__ == "__main__":
    main()