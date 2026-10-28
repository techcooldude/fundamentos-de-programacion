# =====================================================================
# Prototipo inicial - Sistema de Registro y Cobro de Sesiones
# Centro de Fisioterapia y Sanación - Área de Recepción y Caja
# Curso: Solución de problemas con programación computacional
# Avance del Reto/Proyecto (Fase I) - Semana 3
#
# Modelo EPS:
#   Entrada : datos del paciente, servicio, número de sesiones,
#             nivel de dolor, tipo de paciente y forma de pago.
#   Proceso : validaciones, cálculo de subtotal, valoración inicial,
#             descuento aplicable, recargo por tarjeta y acumuladores.
#   Salida  : ticket de cobro, plan de sesiones y corte de caja.
# =====================================================================

# ---------- Constantes (reglas de negocio) ----------
NOMBRE_CENTRO = "Centro de Fisioterapia y Sanación"
CAPACIDAD_DIARIA = 12          # máximo de pacientes atendidos por día

PRECIO_FISIO = 600.0           # 1. Fisioterapia general
PRECIO_DEPORTIVA = 750.0       # 2. Rehabilitación deportiva
PRECIO_SANACION = 500.0        # 3. Terapia de sanación (masaje terapéutico)
PRECIO_ELECTRO = 450.0         # 4. Electroterapia

COSTO_VALORACION = 300.0       # valoración inicial para pacientes de primera vez
MAX_SESIONES = 10              # máximo de sesiones por paquete
SESIONES_PAQUETE = 5           # a partir de 5 sesiones aplica descuento de paquete
DESC_PAQUETE = 0.10            # 10 %
EDAD_ADULTO_MAYOR = 60
DESC_ADULTO_MAYOR = 0.15       # 15 %
RECARGO_TARJETA = 0.03         # 3 % de comisión bancaria
DOLOR_PRIORITARIO = 8          # dolor >= 8 requiere valoración médica prioritaria

# ---------- Acumuladores y contadores del día ----------
pacientes_atendidos = 0
total_efectivo = 0.0
total_tarjeta = 0.0
total_descuentos = 0.0
total_sesiones = 0
casos_prioritarios = 0
cont_fisio = 0
cont_deportiva = 0
cont_sanacion = 0
cont_electro = 0

opcion = ""

print("=" * 55)
print(f"  {NOMBRE_CENTRO}")
print("  Sistema de Registro y Cobro de Sesiones - Recepción")
print("=" * 55)

# ---------- Menú principal (while controlado por opción) ----------
while opcion != "4":
    print("\n----------- MENÚ PRINCIPAL -----------")
    print("1. Registrar atención y cobrar")
    print("2. Ver catálogo de servicios")
    print("3. Corte de caja del día")
    print("4. Salir")
    opcion = input("Elige una opción (1-4): ").strip()

    if opcion == "1":
        # Regla: no se puede exceder la capacidad diaria
        if pacientes_atendidos >= CAPACIDAD_DIARIA:
            print("Capacidad diaria alcanzada. No se pueden registrar más pacientes hoy.")
        else:
            # ---- Entrada: nombre (no vacío) ----
            nombre = input("Nombre del paciente: ").strip()
            while nombre == "":
                print("El nombre no puede estar vacío.")
                nombre = input("Nombre del paciente: ").strip()

            # ---- Entrada: edad válida 1-110 ----
            edad_txt = input("Edad: ").strip()
            while not edad_txt.isdigit() or int(edad_txt) < 1 or int(edad_txt) > 110:
                print("Edad inválida. Debe ser un número entre 1 y 110.")
                edad_txt = input("Edad: ").strip()
            edad = int(edad_txt)

            # ---- Entrada: servicio 1-4 ----
            print("Servicios: 1) Fisioterapia general  2) Rehabilitación deportiva")
            print("           3) Terapia de sanación   4) Electroterapia")
            servicio = input("Servicio (1-4): ").strip()
            while servicio not in ("1", "2", "3", "4"):
                print("Opción de servicio inválida.")
                servicio = input("Servicio (1-4): ").strip()

            if servicio == "1":
                nombre_servicio = "Fisioterapia general"
                precio = PRECIO_FISIO
                cont_fisio += 1
            elif servicio == "2":
                nombre_servicio = "Rehabilitación deportiva"
                precio = PRECIO_DEPORTIVA
                cont_deportiva += 1
            elif servicio == "3":
                nombre_servicio = "Terapia de sanación"
                precio = PRECIO_SANACION
                cont_sanacion += 1
            else:
                nombre_servicio = "Electroterapia"
                precio = PRECIO_ELECTRO
                cont_electro += 1

            # ---- Entrada: número de sesiones 1-MAX_SESIONES ----
            sesiones_txt = input(f"Número de sesiones (1-{MAX_SESIONES}): ").strip()
            while (not sesiones_txt.isdigit() or int(sesiones_txt) < 1
                   or int(sesiones_txt) > MAX_SESIONES):
                print(f"Debe ser un número entre 1 y {MAX_SESIONES}.")
                sesiones_txt = input(f"Número de sesiones (1-{MAX_SESIONES}): ").strip()
            sesiones = int(sesiones_txt)

            # ---- Entrada: nivel de dolor 1-10 ----
            dolor_txt = input("Nivel de dolor reportado (1-10): ").strip()
            while not dolor_txt.isdigit() or int(dolor_txt) < 1 or int(dolor_txt) > 10:
                print("El nivel de dolor debe estar entre 1 y 10.")
                dolor_txt = input("Nivel de dolor reportado (1-10): ").strip()
            dolor = int(dolor_txt)

            # ---- Entrada: ¿primera vez? (booleano) ----
            resp = input("¿Es paciente de primera vez? (s/n): ").strip().lower()
            while resp != "s" and resp != "n":
                resp = input("Responde s o n: ").strip().lower()
            primera_vez = resp == "s"

            # ---- Entrada: forma de pago ----
            pago = input("Forma de pago (E = efectivo, T = tarjeta): ").strip().upper()
            while pago != "E" and pago != "T":
                pago = input("Escribe E o T: ").strip().upper()

            # ---- Proceso ----
            subtotal = precio * sesiones

            valoracion = 0.0
            if primera_vez:
                valoracion = COSTO_VALORACION

            # Regla: los descuentos NO son acumulables; se aplica el mayor
            # (adulto mayor 15 % tiene prioridad sobre paquete 10 %)
            es_adulto_mayor = edad >= EDAD_ADULTO_MAYOR
            es_paquete = sesiones >= SESIONES_PAQUETE
            if es_adulto_mayor:
                porcentaje = DESC_ADULTO_MAYOR
                motivo = "Adulto mayor"
            elif es_paquete:
                porcentaje = DESC_PAQUETE
                motivo = "Paquete de sesiones"
            else:
                porcentaje = 0.0
                motivo = "Sin descuento"

            # El descuento aplica solo a las sesiones, no a la valoración
            descuento = subtotal * porcentaje
            base = subtotal - descuento + valoracion

            recargo = 0.0
            if pago == "T":
                recargo = base * RECARGO_TARJETA
            total = round(base + recargo, 2)

            prioritario = dolor >= DOLOR_PRIORITARIO

            # ---- Acumuladores ----
            pacientes_atendidos += 1
            total_sesiones += sesiones
            total_descuentos += descuento
            if pago == "E":
                total_efectivo += total
            else:
                total_tarjeta += total
            if prioritario:
                casos_prioritarios += 1

            # ---- Salida: ticket ----
            print("\n" + "-" * 45)
            print(f"TICKET #{pacientes_atendidos}  -  {NOMBRE_CENTRO}")
            print("-" * 45)
            print(f"Paciente      : {nombre} ({edad} años)")
            print(f"Servicio      : {nombre_servicio}")
            print(f"Sesiones      : {sesiones} x ${precio:,.2f}")
            print(f"Subtotal      : ${subtotal:,.2f}")
            print(f"Descuento     : -${descuento:,.2f} ({motivo})")
            print(f"Valoración    : ${valoracion:,.2f}")
            print(f"Recargo tarj. : ${recargo:,.2f}")
            print(f"TOTAL A PAGAR : ${total:,.2f}")
            if prioritario:
                print("AVISO: dolor >= 8. Canalizar a valoración médica prioritaria.")
            print("-" * 45)

            # ---- Salida: plan de sesiones (for con recorrido conocido) ----
            print("Plan de sesiones:")
            for numero in range(1, sesiones + 1):
                semana = (numero + 1) // 2      # 2 sesiones por semana
                print(f"  Sesión {numero:2d} -> semana {semana}")

    elif opcion == "2":
        # Catálogo recorrido con for (4 servicios conocidos)
        print("\nCATÁLOGO DE SERVICIOS")
        for i in range(1, 5):
            if i == 1:
                print(f"{i}. Fisioterapia general ......... ${PRECIO_FISIO:,.2f}")
            elif i == 2:
                print(f"{i}. Rehabilitación deportiva ..... ${PRECIO_DEPORTIVA:,.2f}")
            elif i == 3:
                print(f"{i}. Terapia de sanación .......... ${PRECIO_SANACION:,.2f}")
            else:
                print(f"{i}. Electroterapia ............... ${PRECIO_ELECTRO:,.2f}")
        print(f"Valoración inicial (1a vez) ...... ${COSTO_VALORACION:,.2f}")

    elif opcion == "3":
        print("\n========== CORTE DE CAJA ==========")
        if pacientes_atendidos == 0:
            print("Aún no hay pacientes registrados hoy.")
        else:
            total_dia = total_efectivo + total_tarjeta
            ticket_promedio = total_dia / pacientes_atendidos
            print(f"Pacientes atendidos : {pacientes_atendidos} de {CAPACIDAD_DIARIA}")
            print(f"Sesiones vendidas   : {total_sesiones}")
            print(f"Total efectivo      : ${total_efectivo:,.2f}")
            print(f"Total tarjeta       : ${total_tarjeta:,.2f}")
            print(f"TOTAL DEL DÍA       : ${total_dia:,.2f}")
            print(f"Ticket promedio     : ${ticket_promedio:,.2f}")
            print(f"Descuentos otorgados: ${total_descuentos:,.2f}")
            print(f"Casos prioritarios  : {casos_prioritarios}")

            # Servicio más solicitado
            mas_pedido = "Fisioterapia general"
            mayor = cont_fisio
            if cont_deportiva > mayor:
                mas_pedido = "Rehabilitación deportiva"
                mayor = cont_deportiva
            if cont_sanacion > mayor:
                mas_pedido = "Terapia de sanación"
                mayor = cont_sanacion
            if cont_electro > mayor:
                mas_pedido = "Electroterapia"
                mayor = cont_electro
            print(f"Servicio más pedido : {mas_pedido} ({mayor})")

    elif opcion == "4":
        print("Cerrando el sistema. ¡Hasta luego!")

    else:
        print("Opción inválida. Intenta de nuevo.")
