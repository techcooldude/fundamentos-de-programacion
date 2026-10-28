// Sistema de Registro y Cobro de Sesiones
// Centro de Fisioterapia y Sanacion - Area de Recepcion y Caja
// Avance del Reto/Proyecto (Fase I) - Semana 3
Algoritmo RegistroCobroSesiones
	// ----- Constantes (reglas de negocio) -----
	Definir CAPACIDAD, MAX_SESIONES, SESIONES_PAQUETE, EDAD_MAYOR, DOLOR_PRIORITARIO Como Entero
	Definir COSTO_VALORACION, DESC_PAQUETE, DESC_MAYOR, RECARGO_TARJETA Como Real
	CAPACIDAD <- 12
	MAX_SESIONES <- 10
	SESIONES_PAQUETE <- 5
	EDAD_MAYOR <- 60
	DOLOR_PRIORITARIO <- 8
	COSTO_VALORACION <- 300
	DESC_PAQUETE <- 0.10
	DESC_MAYOR <- 0.15
	RECARGO_TARJETA <- 0.03

	// ----- Variables de trabajo -----
	Definir opcion, edad, servicio, sesiones, dolor, i, semana Como Entero
	Definir precio, subtotal, valoracion, porcentaje, descuento, base, recargo, total Como Real
	Definir nombre, nombreServicio, resp, pago, motivo Como Caracter
	Definir primeraVez, esMayor, esPaquete, prioritario Como Logico

	// ----- Acumuladores y contadores -----
	Definir pacientes, totalSesiones, prioritarios, cFisio, cDeportiva, cSanacion, cElectro, mayor Como Entero
	Definir totalEfectivo, totalTarjeta, totalDescuentos, totalDia, promedio Como Real
	Definir masPedido Como Caracter
	pacientes <- 0
	totalSesiones <- 0
	prioritarios <- 0
	cFisio <- 0
	cDeportiva <- 0
	cSanacion <- 0
	cElectro <- 0
	totalEfectivo <- 0
	totalTarjeta <- 0
	totalDescuentos <- 0
	opcion <- 0

	Mientras opcion <> 4 Hacer
		Escribir "----- MENU PRINCIPAL -----"
		Escribir "1. Registrar atencion y cobrar"
		Escribir "2. Ver catalogo de servicios"
		Escribir "3. Corte de caja del dia"
		Escribir "4. Salir"
		Leer opcion

		Segun opcion Hacer
			1:
				Si pacientes >= CAPACIDAD Entonces
					Escribir "Capacidad diaria alcanzada."
				SiNo
					// --- Entradas con validacion ---
					Escribir "Nombre del paciente:"
					Leer nombre
					Mientras Longitud(nombre) = 0 Hacer
						Escribir "El nombre no puede estar vacio:"
						Leer nombre
					FinMientras

					Escribir "Edad (1-110):"
					Leer edad
					Mientras edad < 1 O edad > 110 Hacer
						Escribir "Edad invalida. Ingresa de nuevo:"
						Leer edad
					FinMientras

					Escribir "Servicio: 1) Fisioterapia 2) Rehab. deportiva 3) Sanacion 4) Electroterapia"
					Leer servicio
					Mientras servicio < 1 O servicio > 4 Hacer
						Escribir "Servicio invalido. Ingresa 1-4:"
						Leer servicio
					FinMientras

					Segun servicio Hacer
						1:
							nombreServicio <- "Fisioterapia general"
							precio <- 600
							cFisio <- cFisio + 1
						2:
							nombreServicio <- "Rehabilitacion deportiva"
							precio <- 750
							cDeportiva <- cDeportiva + 1
						3:
							nombreServicio <- "Terapia de sanacion"
							precio <- 500
							cSanacion <- cSanacion + 1
						De Otro Modo:
							nombreServicio <- "Electroterapia"
							precio <- 450
							cElectro <- cElectro + 1
					FinSegun

					Escribir "Numero de sesiones (1-", MAX_SESIONES, "):"
					Leer sesiones
					Mientras sesiones < 1 O sesiones > MAX_SESIONES Hacer
						Escribir "Cantidad invalida. Ingresa de nuevo:"
						Leer sesiones
					FinMientras

					Escribir "Nivel de dolor (1-10):"
					Leer dolor
					Mientras dolor < 1 O dolor > 10 Hacer
						Escribir "Nivel invalido. Ingresa 1-10:"
						Leer dolor
					FinMientras

					Escribir "Es paciente de primera vez? (s/n):"
					Leer resp
					Mientras resp <> "s" Y resp <> "n" Hacer
						Escribir "Responde s o n:"
						Leer resp
					FinMientras
					primeraVez <- resp = "s"

					Escribir "Forma de pago (E/T):"
					Leer pago
					Mientras pago <> "E" Y pago <> "T" Hacer
						Escribir "Escribe E o T:"
						Leer pago
					FinMientras

					// --- Proceso ---
					subtotal <- precio * sesiones
					valoracion <- 0
					Si primeraVez Entonces
						valoracion <- COSTO_VALORACION
					FinSi

					esMayor <- edad >= EDAD_MAYOR
					esPaquete <- sesiones >= SESIONES_PAQUETE
					Si esMayor Entonces
						porcentaje <- DESC_MAYOR
						motivo <- "Adulto mayor"
					SiNo
						Si esPaquete Entonces
							porcentaje <- DESC_PAQUETE
							motivo <- "Paquete de sesiones"
						SiNo
							porcentaje <- 0
							motivo <- "Sin descuento"
						FinSi
					FinSi

					descuento <- subtotal * porcentaje
					base <- subtotal - descuento + valoracion
					recargo <- 0
					Si pago = "T" Entonces
						recargo <- base * RECARGO_TARJETA
					FinSi
					total <- base + recargo
					prioritario <- dolor >= DOLOR_PRIORITARIO

					// --- Acumuladores ---
					pacientes <- pacientes + 1
					totalSesiones <- totalSesiones + sesiones
					totalDescuentos <- totalDescuentos + descuento
					Si pago = "E" Entonces
						totalEfectivo <- totalEfectivo + total
					SiNo
						totalTarjeta <- totalTarjeta + total
					FinSi
					Si prioritario Entonces
						prioritarios <- prioritarios + 1
					FinSi

					// --- Salida: ticket ---
					Escribir "TICKET #", pacientes
					Escribir "Paciente: ", nombre, " (", edad, " anios)"
					Escribir "Servicio: ", nombreServicio
					Escribir "Subtotal: $", subtotal
					Escribir "Descuento: $", descuento, " (", motivo, ")"
					Escribir "Valoracion: $", valoracion
					Escribir "Recargo tarjeta: $", recargo
					Escribir "TOTAL A PAGAR: $", total
					Si prioritario Entonces
						Escribir "AVISO: canalizar a valoracion medica prioritaria."
					FinSi

					// --- Salida: plan de sesiones ---
					Escribir "Plan de sesiones:"
					Para i <- 1 Hasta sesiones Con Paso 1 Hacer
						semana <- trunc((i + 1) / 2)
						Escribir "  Sesion ", i, " -> semana ", semana
					FinPara
				FinSi
			2:
				Escribir "CATALOGO DE SERVICIOS"
				Escribir "1. Fisioterapia general ...... $600"
				Escribir "2. Rehabilitacion deportiva .. $750"
				Escribir "3. Terapia de sanacion ....... $500"
				Escribir "4. Electroterapia ............ $450"
				Escribir "Valoracion inicial (1a vez) .. $", COSTO_VALORACION
			3:
				Escribir "===== CORTE DE CAJA ====="
				Si pacientes = 0 Entonces
					Escribir "Aun no hay pacientes registrados."
				SiNo
					totalDia <- totalEfectivo + totalTarjeta
					promedio <- totalDia / pacientes
					Escribir "Pacientes atendidos: ", pacientes
					Escribir "Sesiones vendidas: ", totalSesiones
					Escribir "Total efectivo: $", totalEfectivo
					Escribir "Total tarjeta: $", totalTarjeta
					Escribir "TOTAL DEL DIA: $", totalDia
					Escribir "Ticket promedio: $", promedio
					Escribir "Descuentos otorgados: $", totalDescuentos
					Escribir "Casos prioritarios: ", prioritarios
					masPedido <- "Fisioterapia general"
					mayor <- cFisio
					Si cDeportiva > mayor Entonces
						masPedido <- "Rehabilitacion deportiva"
						mayor <- cDeportiva
					FinSi
					Si cSanacion > mayor Entonces
						masPedido <- "Terapia de sanacion"
						mayor <- cSanacion
					FinSi
					Si cElectro > mayor Entonces
						masPedido <- "Electroterapia"
						mayor <- cElectro
					FinSi
					Escribir "Servicio mas pedido: ", masPedido, " (", mayor, ")"
				FinSi
			4:
				Escribir "Cerrando el sistema. Hasta luego!"
			De Otro Modo:
				Escribir "Opcion invalida."
		FinSegun
	FinMientras
FinAlgoritmo
